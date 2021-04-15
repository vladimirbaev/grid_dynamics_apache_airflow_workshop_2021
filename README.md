# PiterPy 2020 Apache Airflow Workshop

## Overview
This repository contains Airflow infrastructure setup scripts and example of simple DAG.  
We will use it for building of "Rocket launcher" pipeline.

## Prerequisites
1. [Python 3.6](https://www.python.org/downloads/)
2. [Docker](https://www.docker.com/products/docker-desktop)
3. [Docker Compose](https://docs.docker.com/compose/install/)

## Local environment setup (optional)
Create Python virtual environment:
```
python3 -m venv airflow-workshop-env
source airflow-workshop-env/bin/activate
```

Install packages from `requirements-dev.txt`:
```
pip3 install -r requirements-dev.txt
```

## Airflow setup
1. Run `docker-compose up`
2. Open Airflow Web UI [http://localhost:8080/admin/](http://localhost:8080/admin/)
3. Activate DAG (toggle button near the DAG's name)
3. Click `simple_dag -> Trigger DAG -> Trigger`
4. Go to `Graph View`, check progress and task's logs

## External APIs setup
1. Create [OpenWeatherMap](https://openweathermap.org/appid) account, get API key
2. Create your own [Telegram Bot](https://core.telegram.org/bots#6-botfather)

## Resources
* [Slides](https://github.com/xnuinside/piter_py_2020_apache_airflow/blob/master/slides/PiterPy%202020%20Airflow%20Workshop%20Slides.pdf)
* [Apache Airflow documentation](https://airflow.apache.org/docs/stable/)

## Contacts
Join our [Telegram Group](https://t.me/piter_py_2020_aw) to receive pipeline's notifications

## For Ubuntu Users
Possible, that at the start you will got an error:

PermissionError: [Errno 13] Permission denied: '/opt/airflow/logs/scheduler'

To fix it in docker-compose.yml file change all volumes

  - ./logs:/opt/airflow/logs

to:

  - /opt/airflow/logs


## For Windows 10 Users
If you try to work on Windows 10 & run docker-compose on it you will got an issue for **postgres** service:

FATAL:  data directory "/var/lib/postgresql/data/pgdata" has wrong ownership

To solve this issue you must do additional steps (unfortunately there is no more quick workaround, check: https://forums.docker.com/t/data-directory-var-lib-postgresql-data-pgdata-has-wrong-ownership/17963/23 and https://forums.docker.com/t/trying-to-get-postgres-to-work-on-persistent-windows-mount-two-issues/12456/5?u=friism):

1. Create docker volume:

    docker volume create --name volume-postgresql -d local

2. in docker-compose.yml:
    2.1 add volume at the top of the file, under 'networks' defining like this:

    ``` 
    networks:
      airflow:

    volumes:
      volume-postgresql:
        external: true
    ```

    2.2 change *postgres* service volumes:

        was:  
    ```
      - ./database/data:/var/lib/postgresql/data/pgdata
      - ./database/logs:/var/lib/postgresql/data/log
    ```

        become:
    ```
      - volume-postgresql:/var/lib/postgresql/data/pgdata
      - volume-postgresql:/var/lib/postgresql/data/log
    ```

Or use WSL and run docker under it. 
