# Getting started

Create a .env file in the project root with database config as shown below

```
.
├── soundfront
├── sql
├── tests
├── README.md
└── .env

```

```
export DB_SERVER=localhost,1433
export DB_DATABASE=soundfront
export DB_USERNAME=sa
export DB_PASSWORD='Password'

export FLASK_APP=soundfront
export FLASK_ENV=development
```

Use the following command to start the flask server

```
flask run
```

Use the following command to run tests
```
python -m unittest discover tests
```