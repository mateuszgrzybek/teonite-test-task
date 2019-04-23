# Teonite test task
[![pipeline status](https://gitlab.com/mateuszgrzybek/teonite-test-task/badges/master/pipeline.svg)](https://gitlab.com/mateuszgrzybek/teonite-test-task/commits/master)

Web-scraper for extracting words from https://teonite.com/blog/, storing them in a PostgreSQL DB, and presenting them as stats via Django based REST API. Based on Docker.  

**Tested on macOS Mojave 10.14.1 and Ubuntu 18.04 LTS**  

## tl;dr

1. Clone this repository.
2. Navigate to the repo's root directory.
3. Run:
```
on macOS:
docker-compose up

on linux:
sudo docker-compose up
```
4. Wait for docker to pull all the necessary dependencies and build the images.
5. Watch the containers run (web-scraper may take a short while (averaging 39 seconds) to do it's job, please be patient).
6. After web-scraper is done with it's task (it will exit with code 0), the app is ready to be used on local port 8080.  
You can access the json docs via browsable api or by running `curl` commands such as:

```
curl http://localhost:8080/authors/
curl http://localhost:8080/stats/
curl http://localhost:8080/stats/robertolejnik/
curl http://localhost:8080/stats/michałgryczka/
etc.
```
7. This repository also has GitLab CI enabled. See [**GitLab CI**](#gitlab-ci) paragraph for reference.

## General app info

1. **BeautifulSoup web-scraper**
   * Scraper files are stored in *web-scraper* directory.  
   * The scraper was made using **BeautifulSoup** and **Requests** libraries.  
   * Basic functionality relies on the scraper checking whether the provided website allows a connection. If it does, the script scrapes the first page of the blog looking for it's article urls and each next page's url. The process  repeats on each consecutive page.  
   * After extracting all the urls, it processes the data found on each article's page.  
   * The stats are being calculated within the scraper, before being inserted into the database.  
   * All the scraped words should have special characters and punctuation removed. There also shouldn't be any stop words. **The list of stop words can be manipulated at any time**, by simply editing the list in json file.  
   (see: `word_cleanup(words)` in `web-scraper/scrap.py` and `stop_words.json` in `web-scraper/`)  
   * Dockerfile based on python:3.6 image

2. **PostgreSQL database**
   * Database completely based on a docker image (postgres:9.6).
   * Database tables are created by running Django migrations:
     * `authors` - consists of `author_id` and `author_name` columns, `author_id` being the primary key; stores author id's and corresponding names;
     * `personal_words` - consists of `author_id`, `word` and `word_count` columns; stores author id's and corresponding top 10 words with their count;
     * `total_words` - consists of `word` and `word_count` columns; stores top 10 words across the whole blog and their count;

3. **Django REST API**
   * The api is based on **Django** and **Django REST Framework** (DRF).
   * Most of the files in the *api* directory were created automatically by running `django-admin startproject` and `python3 manage.py startapp`.
   * When the server is running, the app is available on local port 8080.
   * The api returns 3 types of a json document:
     * Authors of the blog posts and their id's at `/authors/` endpoint; ordered alphabetically; ids to be used in the `/stats/<author_id>/` endpoint;
     * Top 10 words and their count across the whole blog at `/stats/` endpoint; ordered by their frequency;
     * Top 10 words and their count per each author at `/stats/<author_id>/` endpoint; ordered by their frequency;
   * Dockerfile based on python:3.6 image

## Docker config

The app uses docker and docker-compose. Docker-compose divides the app into three separate services, which are being  built as images and then bound to containers.  
Both *web-scraper* and *api* have their own Dockerfiles, which are used to build their images.  
The services depend on each other as follows:  
1. The **first** service to be built is the **PostgreSQL database**. It has no dependencies.  
2. The **rest-api** is built next since it **depends on the database** (due to migrations that are supposed to create the tables).  
3. The **last** piece of the app to be built is the **web-scraper**. Since it's job is to insert the data into the previously created tables, it's **dependencies contain both the database and rest-api**.

Since defining dependencies doesn't mean the services actually wait for each other, plenty of solutions were tried. In the end, the best one seemed to be https://github.com/ufoscout/docker-compose-wait. It simply waits for a TCP port on a certain image to be open.  
Adding waiting wasn't actually necessary since the app seemed to be running properly anyway, although the log was quite messy.

## GitLab CI

This app has a registered GitLab CI Runner, which lives in *gitlab-runner* directory. In order for it to be able to run pipelines it has to be turned on locally via `docker-compose`.  
To make it's magic possible, user has to navigate to the 'gitlab-runner' directory and run:
```
docker-compose up -d
```
After the runner is built, all changes that are commited and pushed to the GitLab remote will be checked by the pipeline.  
There are two defined stages in the `.gitlab-ci.yml` file:
1. Automatically building docker images for *web-scraper* and *api*.
2. Pushing the created images to the author's DockerHub (only if the first job is succesful).

If both jobs pass, the pipeline gets marked as passing.  

**NOTE: The GitLab CI is configured to use two environment variables - REGISTRY_USER and REGISTRY_PASSWORD, both of them being Dockerhub login credentials.**  
**In order for everything to work seamlessly it is required that these variables are defined in GitLab's settings (CI/CD/Variables).**

**NOTE 2: Since the configured runner is a specific-type runner, it won't be cloned while forking the repository (unlike a shared one). In this case the best way for the CI to work among a group of users would be forking the main repository, commiting changes to the forked one and then opening a pull request to the main one. The changes would be then checked by the pipeline.**

## App's workflow

1. `docker-compose up` reads `docker-compose.yml` and builds all defined services in the way described in *Docker config*;
2. Services start, but wait for each other
   * **Postgres starts first**
   * **Django makes migrations** into it **and starts running on port 8080**;  
   * In the end **scraper gets all the data and inserts it into the database**, which can then be viewed via the api;
3. The app is ready to use. Desired json docs can be accessed either via `curl` commands such as:
```
curl http://localhost:8080/authors/
curl http://localhost:8080/stats/
curl http://localhost:8080/stats/robertolejnik/
curl http://localhost:8080/stats/michałgryczka/
etc.
```
or via browsable api, which can be accessed by simply entering the above urls into the browser.
