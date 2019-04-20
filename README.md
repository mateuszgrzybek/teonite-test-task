# Teonite test task

Web-scraper for extracting words from https://teonite.com/blog/, storing them in a PostgreSQL DB, and presenting them as stats via Django based REST API. Based on Docker.  

**Tested on macOS Mojave 10.14.1 and Ubuntu 18.04 LTS**  

## tl;dr

1. Navigate to the repo's root directory
2. Run:
```
on macOS:
docker-compose up

on linux:
sudo docker-compose up
```
3. Wait for docker to pull all the necessary dependencies and build the images.
4. Watch containers run (web-scraper may take a short while to do it's job, please be patient).
5. After web-scraper is done with it's task, the app is ready to be used on local port 8080.  
You can access the json docs via browsable api or by running `curl` commands such as:
```
curl http://localhost:8080/authors/
curl http://localhost:8080/stats/
curl http://localhost:8080/stats/robertolejnik/
curl http://localhost:8080/stats/michałgryczka/
etc.
```

## General app info

1. **BeautifulSoup web-scraper**
   * Scraper files are stored in *web-scraper* directory.  
   * The scraper was made using **BeautifulSoup** and **Requests** libraries.  
   * Basic functionality relies on the scraper checking whether the provided website allows a connection. If it does, the script scrapes the first page  
   of the blog looking for it's article urls and each next page's url.  
   * After extracting all the urls, it processes the data found on each article's page.  
   * The stats are being calculated within the scraper, before being inserted into the database.  
   * All the scraped words should have special characters and punctuation removed. There also shouldn't be any urls or stop words  
   (see: `word_cleanup(words)` in `web-scraper/scrap.py`)  
   * Dockerfile based on python:3.6 image

2. **PostgreSQL database**
   * Database completely based on a docker image (postgres:9.6).
   * Database tables are created by running Django migrations:
     * `authors` - consists of `author_id` and `author_name` columns, `author_id` being the primary key; stores author id's and corresponding names;
     * `personal_words` - consists of `author_id`, `word` and `word_count` columns; stores author id's and corresponding top 10 words with their count;
     * `total_words` - consists of `word` and `word_count` columns; stores top 10 words accross the whole blog and their count;

3. **Django REST API**
   * The api is based on **Django** and **Django REST Framework** (DRF).
   * Most of the files in the *api* directory were created automatically by running 'django-admin startproject' and 'python3 manage.py startapp'.
   * When the server is running, the app is available on local port 8080.
   * The api returns 3 types of json document:
     * Authors of the blog posts and their id's at `/authors/` endpoint; ordered alphabetically; ids to be used in the `/stats/<str:author_id>/` endpoint;
     * Top 10 words and their count accross the whole blog at `/stats/` endpoint; ordered by their frequency;
     * Top 10 words and their count per each author at `/stats/<author_id>/` endpoint; ordered by their frequency;
   * Dockerfile based on python:3.6 image

## Docker config

The app uses docker images and docker-compose. Docker-compose divides the app into three separate services, although they depend on each other.  
1. The **first** service to be built is the **PostgreSQL database**. It has no dependencies.  
2. The **rest-api** is built next since it **depends on the database** (due to migrations that are supposed to create the tables).  
3. The **last** piece of the app to be built is the **web-scraper**. Since it's job is to insert the data into the previously created tables,  
it's **dependencies contain both the database and rest-api**.

Since defining dependencies doesn't mean the services actually wait for each other, plenty of solutions were tried. In the end, the best one seemed to be
https://github.com/ufoscout/docker-compose-wait. It simply waits for a TCP port on a certain image to be open.  
Adding waiting wasn't actually necessary since the app seemed to be running properly anyway, although the log was quite messy.

## GitLab CI

This app has a registered GitLab CI Runner, which lives in 'gitlab-runner' directory. In order for it to be able to run pipelines it has to be turned on locally via docker-compose.  
To make it's magic possible, simply navigate to the 'gitlab-runner' directory and run:
```
docker-compose up -d
```
After the runner is built, all changes that are commited and pushed to the GitLab remote will be checked by the pipeline.  
There are two defined stages in the `.gitlab-ci.yml` file. First one is responsible for automatically building the docker images (`web-scraper` and `rest-api`).  
If the job passes, the second stage begins. It's main goal is to push the created images to author's dockerhub.  
If both jobs pass, the commit also gets marked as passed.  

## App's workflow

1. `docker-compose up` reads `docker-compose.yml` and builds all defined services in the way described in *Docker config*;
2. Services wait for each other
   * **Postgres starts first**
   * **Django makes migrations** into it **and starts running on port 8080**;  
   * in the end **scraper gets all the data and inserts it into the database**, which can then be viewed via the api;
3. The app is ready to use. Desired json docs can be accessed either via `curl` commands such as:
```
curl http://localhost:8080/authors/
curl http://localhost:8080/stats/
curl http://localhost:8080/stats/robertolejnik/
curl http://localhost:8080/stats/michałgryczka/
etc.
```
or via browsable api, which can be accessed by simply entering the above urls into the browser.

