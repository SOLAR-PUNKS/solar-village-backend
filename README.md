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
- `./run_migrations.sh` (⚠️ **Important:** Always use this script, not `python manage.py migrate` directly)
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

This application supports two authentication methods:

### Username/Password Authentication

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

### Passkey Authentication (Passwordless)

This application supports passwordless authentication using WebAuthn passkeys (Apple Passkeys, Android device authentication, or security keys). Users can authenticate using device biometrics without requiring a password.

#### Registration Flow

1. **Register a passkey**: Users must first register a passkey using the django-otp-webauthn registration endpoints at `/webauthn/register/`. This typically requires:
   - User to be logged in (or create an account first)
   - Browser support for WebAuthn
   - Device with biometric authentication or security key

2. **Complete registration**: The frontend will handle the WebAuthn registration flow using the browser's Web Authentication API.

#### Authentication Flow

1. **Initiate authentication**: The client initiates passkey authentication using the django-otp-webauthn endpoints at `/webauthn/login/`.

2. **Complete authentication**: The user authenticates using their device's biometric sensor or security key.

3. **Get JWT tokens**: After successful passkey authentication, call `/api/webauthn/token/` to receive JWT tokens:
```
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=<session_id>" \
  http://localhost:8000/api/webauthn/token/
```

The response will return an "access" key containing the JWT and a "refresh" key with the refresh token, in the same format as username/password authentication. Subsequent requests to the API should send an HTTP `Authentication` header with the value `Bearer <access/JWT>`.

#### Requirements

- **HTTPS in production**: WebAuthn requires HTTPS in production environments (localhost is allowed for development)
- **Browser compatibility**: Passkeys are supported in modern browsers (Chrome 67+, Firefox 60+, Safari 13+, Edge 18+)
- **Domain configuration**: The `ALLOWED_HOST` environment variable must be set correctly for production

#### Notes

- Users can register multiple passkeys (devices)
- Passkey authentication is passwordless - no password is required
- JWT tokens from passkey authentication are compatible with the existing API authentication system
- Username/password authentication remains available alongside passkeys
