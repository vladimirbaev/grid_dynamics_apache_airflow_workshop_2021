FROM apache/airflow:1.10.11
COPY requirements.txt /
USER airflow
RUN pip install --user -r /requirements.txt
