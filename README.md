<div id="top"></div>

<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/hoaktran/postgresql-to-bigquery-etl">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">postgresql-to-bigquery-etl</h3>

  <p align="center">
    `postgresql-to-bigquery-etl` migrates the data from PostgreSQL to Google BigQuery periodically and incrementally.
    <br />
    <a href="https://github.com/hoaktran/postgresql-to-bigquery-etl"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/hoaktran/postgresql-to-bigquery-etl/issues">Report Bug</a>
    ·
    <a href="https://github.com/hoaktran/postgresql-to-bigquery-etl/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#logic">Logic</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

PostgreSQL is one of the most popular tools to store and analyze data at scale. However, it requires a huge effort and expertise to run analytic queries within the desired time using PostgreSQL. 

This is a barrier for non-expert business users. A solution is to  have a separate system on the cloud for analytical workloads to allow additional benefits like automatic and elastic scaling based on the complexity of queries.

Hence, I created this code to mirror data from PostgreSQL to Google BigQuery.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [![Google Cloud][Google Cloud.js]][Google Cloud-url]
* [![PostgreSQL][PostgreSQL.js]][PostgreSQL-url]
* [![Python][Python.js]][Python-url]

<p align="right">(<a href="#top">back to top</a>)</p>

### Logic
* Get all the tables within the specified database on PostgreSQL
* For each PostgreSQL table
  * If it has not existed on BigQuery, then save the whole table to a CSV file, and upload it to BigQuery under the name `final_{table_name}`
  * If it has already existed on BigQuery
    * If it does not have the field on update timestamp or the table schema has changed, then save the whole table to a CSV file, and upload it to BigQuery under the name `final_{table_name}`
    * If it has the field on update timestamp and the table schema has not changed, then get the lastest update timestamp of the respective table on BigQuery, and divide the table into two parts
      * The first part is the rows that have not been updated since the previous sync
        * Save this part to a CSV file and upload it to BigQuery under the name `intermediate_not_updated_{table_name}`
        * Delete all rows on the respective BigQuery table if they do not appear in the table `intermediate_not_updated_{table_name}` (because these are the deleted or updated rows)
      * The second part is the rows that have been updated or inserted since the previous sync
        * Save this part to a CSV file and upload it to BigQuery under the name `intermediate_updated_{table_name}`
        * Insert all rows from the table `intermediate_updated_{table_name}` to the respective BigQuery table

It is worth to talk a bit about uploading a CSV file to a BigQuery table. Theoretically, BigQuery can automatically detect the schema from the file. However, it only scan up to the first 500 rows of the file to dertemine the data type. This can break the code if later on, the data does not have the same type. Another workaround way is to assign the schema for each CSV file specifically, which is a huge hassle. Therefore, I decide to, whenever uploading a CSV file to a BigQuery table, converting all the fields to the string format.

Finally, the code will check the update timestamp in each `intermediate_not_updated_{table_name}`, if available, and send the alert email if the data is stale.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

1. Create a service account for BigQuery API following [this article](https://cloud.google.com/bigquery/docs/reference/libraries) and download it to local environment
2. Clone the repo
   ```sh
   git clone https://github.com/hoaktran/postgresql-to-bigquery-etl.git
   ```
3. Install the necessary libraries from `requirements.txt`
   ```sh
   pip install requirements.txt
   ```
4. Set an environment variable for BigQuery API in `etl.py`
   ```py
   working_folder = os.getcwd()
   client = bigquery.Client.from_service_account_json(os.sep.join([working_folder, "bigqueryapi.json"]))
   ```
5. For the sending alert email function when the data gets stale, set the sender and receiver emails, along with the app password if they are gmail (tips can be found [here](https://support.google.com/accounts/))
  ```py
  def send_email_notification(subject, content):
    sender_email = "the-sender-email@gmail.com"
    app_password = "app-password" 
    receiver_email = "the-receiver-email@gmail.com"
  ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

For a specific environment, you can run the function `mirror(env)` to mirror that environment from Postgres to BigQuery.

To get notification on stale data, run the function `stale_notify(env)`.


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Add `apscheduler` library to schedule cron job
- [ ] Explore other options to migrate data in real time, for example [using Google Cloud Dataflow](https://cloud.google.com/bigquery/docs/migration/redshift-overview)

See the [open issues](https://github.com/hoaktran/postgresql-to-bigquery-etl/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Hoa Tran - hoaktran38@gmail.com

Project Link: [https://github.com/hoaktran/postgresql-to-bigquery-etl](https://github.com/hoaktran/postgresql-to-bigquery-etl)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [psycopg2 library](https://pypi.org/project/psycopg2/)
* [Hevo data blog on PostgreSQL to BigQuery ETL](https://hevodata.com/blog/postgresql-to-bigquery-data-migration/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/hoaktran/postgresql-to-bigquery-etl.svg?style=for-the-badge
[contributors-url]: https://github.com/hoaktran/postgresql-to-bigquery-etl/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/hoaktran/postgresql-to-bigquery-etl.svg?style=for-the-badge
[forks-url]: https://github.com/hoaktran/postgresql-to-bigquery-etl/network/members
[stars-shield]: https://img.shields.io/github/stars/hoaktran/postgresql-to-bigquery-etl.svg?style=for-the-badge
[stars-url]: https://github.com/hoaktran/postgresql-to-bigquery-etl/stargazers
[issues-shield]: https://img.shields.io/github/issues/hoaktran/postgresql-to-bigquery-etl.svg?style=for-the-badge
[issues-url]: https://github.com/hoaktran/postgresql-to-bigquery-etl/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/hoa-tran-730b40133
[Python.js]: https://img.shields.io/badge/python-306998?style=for-the-badge&logo=python&logoColor=ffd438
[Python-url]: https://python.org/
[PostgreSQL.js]: https://img.shields.io/badge/PostgreSQL-0769AD?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Google Cloud.js]: https://img.shields.io/badge/google%20cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white
[Google Cloud-url]: https://cloud.google.com/
