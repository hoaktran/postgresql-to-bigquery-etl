<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


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
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
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

This is a barrier for business users who do not have that skill. This is why it is preferred to have a separate system on the cloud for analytical workloads, so we can have additional benefits like automatic and elastic scaling based on the complexity of queries. 

Hence, I choose to mirror data from PostgreSQL to Google BigQuery.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [![Google Cloud][Google Cloud.js]][Google Cloud-url]
* [![PostgreSQL][PostgreSQL.js]][PostgreSQL-url]
* [![Python][Python.js]][Python-url]

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/hoaktran/postgresql-to-bigquery-etl.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

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

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/hoaktran/postgresql-to-bigquery-etl](https://github.com/hoaktran/postgresql-to-bigquery-etl)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

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
[license-shield]: https://img.shields.io/github/license/hoaktran/postgresql-to-bigquery-etl.svg?style=for-the-badge
[license-url]: https://github.com/hoaktran/postgresql-to-bigquery-etl/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Python.js]: https://img.shields.io/badge/python-306998?style=for-the-badge&logo=python&logoColor=ffd438
[Python-url]: https://python.org/
[PostgreSQL.js]: https://img.shields.io/badge/PostgreSQL-0769AD?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Google Cloud.js]: https://img.shields.io/badge/google%20cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white
[Google Cloud-url]: https://cloud.google.com/
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
