# %%
### Import libraries ###
import psycopg2, io, os, shutil, yagmail
import pandas as pd
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from datetime import datetime, timezone
from time import time

working_folder = os.getcwd()
client = bigquery.Client.from_service_account_json(os.sep.join([working_folder, "your-bigquery-access-token-file.json"]))

### Set necessary variables ###
download_folder = os.sep.join([working_folder, "BigQuery Sync"])
bq_project_id = "your-bigquery-project-id"
postgres_db_name = "your-postgres-database-name"

env_creds = {}

i = 1
while True:
    name        = f"NAME{i}"
    host        = f"HOST{i}"
    user        = f"USER{i}"
    password    = f"PASSWORD{i}"
    port        = f"PORT{i}"
    
    if (name not in os.environ
        or host not in os.environ
        or user not in os.environ
        or password not in os.environ
        or port not in os.environ):
        break

    dbConfig = {
        "host": os.environ[host],
        "user": os.environ[user],
        "password": os.environ[password],
        "port": os.environ[port]
    }
    env_creds[os.environ[name]] = dbConfig
    i += 1

### Define necessary functions ###
def timer_func(func):
    """Shows the execution time of the function object passed.
    """
    def wrap_func(*args):
        t1 = time()
        result = func(*args)
        t2 = time()
        print(f"Function {func.__name__!r} with arguments {args} executed in {(t2-t1):.2f}s.")
        return result
    return wrap_func

def is_folder_existing(folder_path):
    """Checks to see if a folder has existed or not.
    If not, creates one.

    Args:
        folder_path (str): The absolute folder path of which existence need to be checked
    """
    if os.path.isdir(folder_path):
        pass
    else:
        os.makedirs(folder_path)
        print(f"The folder {folder_path} has just been created.")

def generate_bq_table_name(table_type, table_name):
    """Generates the table name on BigQuery based on the given 
    table_type and table_name.

    Args:
        table_type (str): It can be either "delete", "intermediate" or "final".
        table_name (str): The 

    Returns:
        str: The table name on BigQuery
    """
    bq_table_name = f"{table_type}_{table_name}"
    return bq_table_name

def generate_bq_dataset_name(env, table_type):
    bq_dataset_name = f"{table_type}_{env}"
    return bq_dataset_name

def generate_bq_dataset_id(env, table_type):
    bq_dataset_id = f"{bq_project_id}.{generate_bq_dataset_name(env, table_type)}"
    return bq_dataset_id

def generate_bq_table_id(env, table_type, table_name):
    bq_table_id = f"{generate_bq_dataset_id(env, table_type)}.{generate_bq_table_name(table_type, table_name)}"
    return bq_table_id

def is_bq_dataset_existing(env, table_type):
    """Checks to see if a dataset has existed on BigQuery or not.
    If not, creates one.
    """
    try:
        client.get_dataset(generate_bq_dataset_id(env, table_type))
    except NotFound:
        dataset = bigquery.Dataset(generate_bq_dataset_id(env, table_type))
        dataset.location = "US"
        dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
        print(f"Created dataset `{generate_bq_dataset_id(env, table_type)}`")

def load_to_df(query):
  """Returns a dataframe loaded from the query result.

  Args:
      query (multi-line string): The SQL query

  Returns:
      dataframe: The dataframe saved from the query result
  """
  query_job = client.query(query)
  query_job.result()
  df = query_job.to_dataframe()
  return df

def create_schema_from_csv(env, table_type, table_name):
  """Creates a BQ table schema from a CSV file.

  All fields in the schema is in string type.

  Args:
      file_name (str): The file name without extension that we want to get the schema

  Returns:
      BigQuery schema: The output schema get from the CSV file
  """
  df = pd.read_csv(os.sep.join([download_folder, env, generate_bq_dataset_name(env, table_type),f"{generate_bq_table_name(table_type, table_name)}.csv"]), nrows=0)
  schema = []
  for i in df.columns:
      schema.append(bigquery.SchemaField(i, "STRING"))
  return schema

@timer_func
def establish_connection_to_postgres(env):
    """ Returns the environment connection from AWS RDS on Postgres. 
    
    Args:
        env (str): 
    """
    env_cred = env_creds[env]
    conn = psycopg2.connect(
        host = env_cred["host"], 
        user = env_cred["user"], 
        password = env_cred["password"], 
        port = env_cred["port"], 
        dbname = postgres_db_name
    )
    return conn

# %%
@timer_func
def export_one_postgres_table(curs, env, table_name):
    """Exports one Postgres table to a local CSV file.

    If the final table hasn't existed on BQ and the table schema between Postgres and BQ match,
    then the entire Postgres table will be exported.
    Otherwise, only the latest updated data from the Postgres table will be exported.

    Args:
        curs (Postgres cursor): The Postgres cursor that depends on the chosen environment. 
        env (str): The chosen database on Postgres.
        table_name (str): Name of the Postgres table
    """
    # Check if the download directory for the chosen env exists or not
    # if not, create one
    for table_type in ["intermediate_not_updated", "intermediate_updated", "final"]:
        is_folder_existing(os.sep.join([download_folder, env, generate_bq_dataset_name(env, table_type)]))

    # Set the Postgres query 
    def get_column_list(table_name):
        """Returns the column list of the table.
        """
        curs.execute(f"SELECT * FROM {table_name} LIMIT 0")
        column_names = [desc[0] for desc in curs.description]
        return column_names

    sql_query = f"COPY (SELECT * FROM {table_name}) TO STDOUT WITH CSV HEADER"    
    table_type = "final"

    try:
        client.get_table(generate_bq_table_id(env, "final", table_name))

        postgres_table_column_list = get_column_list(table_name)
        musicdb_table_column_list = load_to_df(
            f"""
            SELECT
                column_name
            FROM `{generate_bq_dataset_id(env, "final")}`.INFORMATION_SCHEMA.COLUMNS
            WHERE table_name = "{generate_bq_table_name("final", table_name)}"
            """
        )["column_name"].to_list()

        # Only check the last time update and download data into the intermediate table
        # when the table schema between Postgres and BQ match, 
        # and the column "updated_at" exists in the Postgres table
        if postgres_table_column_list == musicdb_table_column_list and "updated_at" in postgres_table_column_list:
            last_time_update = load_to_df(
                f"""
                SELECT
                    COALESCE(MAX(updated_at), "1900-01-01") last_time_update
                FROM `{generate_bq_table_id(env, "final", table_name)}`
                """
            )["last_time_update"][0]
            # don't use double quote in Postgres query
            sql_query = f"COPY (SELECT * FROM {table_name} WHERE updated_at > '{last_time_update}') TO STDOUT WITH CSV HEADER"
            table_type = "intermediate_updated"

            with io.open(
                os.sep.join([
                    os.sep.join([download_folder, env]),
                    generate_bq_dataset_name(env, "intermediate_not_updated"),
                    f"""{generate_bq_table_name("intermediate_not_updated", table_name)}.csv"""
                ]),
                "w",
                encoding="utf-8-sig"
            ) as output:
                # don't use double quote in Postgres query
                curs.copy_expert(f"COPY (SELECT id FROM {table_name} WHERE updated_at <= '{last_time_update}') TO STDOUT WITH CSV HEADER", output)
    
    except NotFound:
        pass

    # Execute the command to save the query to a local CSV file
    with io.open(
        os.sep.join([
            os.sep.join([download_folder, env]),
            generate_bq_dataset_name(env, table_type),
            f"{generate_bq_table_name(table_type, table_name)}.csv"
        ]),
        "w",
        encoding="utf-8-sig"
    ) as output:
        curs.copy_expert(sql_query, output)

# %%
def export_all_postgres_tables(env):
    """Exports all Postgres tables of the chosen environment to local CSV files.

    Postgres connection would be established one time only and close when done.
    The local folder used to save downloaded CSV files need to be cleared before the download.

    Args:
        env (str): The chosen database on Postgres.
    """
    conn = establish_connection_to_postgres(env)
    curs = conn.cursor()

    # List all the tables in the env database
    curs.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = [r[0] for r in curs.fetchall()]

    download_env_folder = os.sep.join([download_folder, env])

    # Remove the download_env_folder and all of its files if it has already existed
    shutil.rmtree(download_env_folder, ignore_errors=True)

    # Export tables
    for table_name in tables:
        export_one_postgres_table(curs, env, table_name)

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    curs.close()
    conn.close()
        

# %%
@timer_func
def load_one_csv_file_to_bq(env, table_type, table_name):
    """Loads a local CSV file to a BigQuery table.
    """
    # Check if the dataset for the env and table_type has existed yet,
    # if not, create one.
    is_bq_dataset_existing(env, table_type)

    with io.open(os.sep.join([download_folder, env, generate_bq_dataset_name(env, table_type), f"{generate_bq_table_name(table_type, table_name)}.csv"]), "rb") as source_file:
        schema = create_schema_from_csv(env, table_type, table_name)
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV, 
            skip_leading_rows=1, 
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE, 
            allow_jagged_rows=True,
            allow_quoted_newlines=True,
            schema=schema
        ) 
        job = client.load_table_from_file(
            source_file, 
            generate_bq_table_id(env, table_type, table_name), 
            job_config=job_config
        )
        job.result()
    
# %%
def load_csv_files_from_one_table_type_to_bq(env, table_type):
    """Loads all CSV files of a table type ("intermediate" or "final")
    to the respective BigQuery dataset.
    """
    # Check if the dataset for the env and table_type has existed yet,
    # if not, create one.
    is_bq_dataset_existing(env, table_type)

    download_env_table_type_folder = os.sep.join([download_folder, env, generate_bq_dataset_name(env, table_type)])
    files = os.listdir(download_env_table_type_folder)
    if len(files) > 0:
        for file_name in files:
            table_name = file_name.split(".")[0][(len(table_type)+1):]
            load_one_csv_file_to_bq(env, table_type, table_name)

# %%
def load_all_csv_files_to_bq(env):
    """Loads all CSV files from both "intermediate" and "final" table types
    of a chosen environment to the respective BigQuery datasets.
    """
    for table_type in ["intermediate_not_updated", "intermediate_updated", "final"]:
        load_csv_files_from_one_table_type_to_bq(env, table_type)

@timer_func
def update_bq_final_table_from_intermediate_not_updated_table(env, table_name):
    """Deletes rows in the final table that don't appear in the delete table.
    """
    try:
        job = client.query(
            f"""
            DELETE `{generate_bq_table_id(env, "final", table_name)}` final
            WHERE final.id NOT IN (
                SELECT
                    id
                FROM `{generate_bq_table_id(env, "intermediate_not_updated", table_name)}`
            )
            """
        )
        job.result()

    except NotFound:
        print(f"""The table `{generate_bq_table_id(env, "intermediate_not_updated", table_name)}` doesn't exist.""")

# %%
@timer_func
def update_bq_final_table_from_intermediate_updated_table(env, table_name):
    """Updates a BigQuery final table from its respective intermediate table.

    If the intermediate table doesn't have any row, take no action.
    Otherwise, insert the whole intermediate table into the final table.

    Args:
        env (str): The chosen database on Postgres. It can be either "musicdb_dev", "musicdb_prod", or "msk".
        table_name: Name of the Postgres table
    """
    try:
        intermediate_table = client.get_table(generate_bq_table_id(env, "intermediate_updated", table_name))

        if intermediate_table.num_rows != 0:
            job = client.query(
                f"""
                INSERT `{generate_bq_table_id(env, "final", table_name)}`
                SELECT
                    *
                FROM  `{generate_bq_table_id(env, "intermediate_updated", table_name)}`
                """
            )
            job.result()
    
    except NotFound:
        print(f"""The table `{generate_bq_table_id(env, "intermediate_updated", table_name)}` doesn't exist.""")


# %%
def update_all_bq_final_tables(env):
    """Updates all BigQuery final tables of the chosen environment
    from their respective intermediate tables.

    Args:
        env (str): The chosen database on Postgres. It can be either "musicdb_dev", "musicdb_prod", or "msk".
    """
    for table in client.list_tables(generate_bq_dataset_id(env, "intermediate_updated")):
        table_name = table.table_id[(len("intermediate_updated")+1):]
        update_bq_final_table_from_intermediate_not_updated_table(env, table_name)
        update_bq_final_table_from_intermediate_updated_table(env, table_name)

# %%
def mirror(env):
    """Mirrors all tables of the chosen environment
    from Postgres to BigQuery.

    The result is in the BigQuery dataset "final_{env}".

    Args:
        env (str): The chosen database on Postgres. It can be either "musicdb_dev", "musicdb_prod", or "msk".
    """
    export_all_postgres_tables(env)
    load_all_csv_files_to_bq(env)
    update_all_bq_final_tables(env)

def get_stale_tables(env):
    """Returns a dictionary of key-value pairs with keys are BQ tables that their last modified dates
    , which are also their respective keys, are more than two days ago.

    Args:
        env (str): It can be either "musicdb_dev", "musicdb_prod", or "msk".
    """
    bq_dataset_id = f"{bq_project_id}.intermediate_updated_{env}"
    dataset = client.get_dataset(bq_dataset_id)
    table_list = list(client.list_tables(dataset))
    last_update_dict = dict()
    for table_item in table_list:
        table = client.get_table(table_item.reference)
        last_update = table.modified # this is an offset-aware datetime 
        now = datetime.now(timezone.utc) # this need to be an offset-aware datetime too
        day_difference = (now - last_update).days
        if day_difference > 2: 
            last_update_dict[table.table_id] = last_update.strftime("%Y-%m-%d")
    return last_update_dict

def send_email_notification(subject, content):
    """Sends an email notification with the specified subject and content
    from the sender email to the receiver email.

    Args:
        subject (str): The email subject
        content (list): A list of string that makes the email content lines
    """
    sender_email = "the-sender-email-address@gmail.com"
    app_password = "your-sender-email-app-password" # app password for gmail
    receiver_email = "the-receiver-email-address@gmail.com"

    try:
        with yagmail.SMTP(sender_email, app_password) as yag:
            yag.send(receiver_email, subject, content)
    except Exception as e:
        print(f"Sending email notification failed with error: {e}")
    else:
        print("Sent email successfully")  

def stale_notify(env):
    stale_tables = get_stale_tables(env)
    if len(stale_tables) > 0:
        send_email_notification(
            subject=f"BQ mirror stale data alert: env {env}", 
            content=[stale_tables]
        )

def executeJob():
    # # %%
    for env in env_creds.keys():
        try:
            mirror(env)
        except Exception as e:
            send_email_notification(
                subject=(f"BQ mirror update alert: env {env}"),
                content=[e]
            )

        stale_notify(env)