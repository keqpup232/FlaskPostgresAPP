# Documentation:
## Running the application locally
```textmate
chmod +x ./flask_app/init-user-db.sh
docker compose up -d
```
App start to http://localhost:8000, you can fill in form your "name" and "email" then check if it works. <br>
Next you see your added data at http://localhost:8000/last5users, this means everything is working.
## Useful links
- [digitalocean postgres+flask](https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application#prerequisites)
- [docker postgres](https://hub.docker.com/_/postgres)
## Useful commands
```textmate
docker exec -it postgres bash #connect docker container named 'postgres'
su postgres
psql #terminal client
CREATE DATABASE flask_db;
CREATE USER sammy WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE flask_db TO sammy;
\c flask_db postgres #connect db
GRANT ALL ON SCHEMA public TO sammy;
\l #check
\q
pip install Flask psycopg2-binary
flask run
```
## Test documentation
- [flask test selenium](https://gpttutorpro.com/how-to-use-flask-testing-to-write-unit-tests-for-your-web-application/)
- [flask LiveServerTestCase](https://flask-testing.readthedocs.io/en/latest/)

Local env to run tests
```textmate
POSTGRES_DB=flask_db;
POSTGRES_PASSWORD=password;
POSTGRES_USER=sammy;
HOST_ENV=localhost;
```
Commands to start tests
```textmate
python -m app_test_unit.py
```