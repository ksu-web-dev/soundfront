FROM zerogjoe/mssql-python3.6-pyodbc

ADD . /app
WORKDIR /app
RUN pip install -r soundfront/requirements.txt

CMD ["flask", "run"]
