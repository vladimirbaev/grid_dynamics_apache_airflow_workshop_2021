FROM apache/airflow:1.10.14
COPY requirements.txt /
USER airflow
RUN pip install --user -r /requirements.txt
