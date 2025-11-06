# Solar Village Backend

## Pre-release go-backs
- If we're doing a container for deployment, we must know what the https situation is and ensure that it's implemented.
- The Gunicorn settings in gunicorn.conf.py should be given a look over for prod suitability 

## Prerequisites
- Python must be installed (Python 13 for now, though python14 is unlikely to hurt anything)
- Docker compose must be installed
- For first time setup, run these commands locally:
    - `python -m venv venv`
    - Activate the virtual environment with
        - Windows: `venv\Scripts\activate`
        - Linux/bash: `source venv/bin/activate`
    - `pip install -r requirements.txt`

## Running the application
- `docker-compose up --build --detach`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`

Development server will be available at `http://localhost:8000/api/`. The development server will restart on file changes for quick development.
PGAdmin will be available at `http://localhost:8081` and can be logged in using `postgres@postgres.com`/`postgres`. The database is also `postgres` for name `postgres` for password. These are driven by the environment variables in the docker-compose. 

The application's packaged/dockerized version will be available at `http://localhost/api/`. This instance of the application will only change after each `docker-compose up --build` command so the development server is more helpful during development due to quick feedback. However, it's good to check this in the end to ensure that any settings/changes work properly outside of the development server.

## Tear down
`docker-compose down` to bring the application down.
`docker-compose down --volumes` to delete the database for a fresh start.

## Linting
Run `pycodestyle .` to run the linter. `tox.ini` defines the linter config.

## Authentication
This application uses simplejwt to receive username/password and return a Json Web Token. Send a POST request to http://localhost:8000/api/token/ (for development) such as in this curl example:
```
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password"}' \
  http://localhost:8000/api/token/
```
The response will return an "access" key containing the JWT and a "refresh" key with the refresh token. Subsequent requests to the api should send an HTTP `Authentication` header with the value `Bearer <access/JWT>`. If the access token has expired but the refresh token has not yet expired, a new token can be obtained by sending a request to http://localhost:8000/api/token/refresh/, as in this curl example:
```
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<the full JWT>"}' \
  http://localhost:8000/api/token/refresh/

```

### Some informal TODO items
- Postgres is up, but we'll most likely need postgis so look into that.
- Do username/password JWT auth for now.
