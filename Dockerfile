FROM python:3.13-slim

# Install system dependencies for GDAL and PostGIS
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        binutils \
        libproj-dev \
        gdal-bin \
        libgdal-dev \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN python3 -m pip install --no-cache-dir gunicorn==23.0.0

COPY . .

RUN python3 manage.py collectstatic --noinput

# Run migrations on container startup (ensures core.User is created before admin migrations)
CMD ./run_migrations.sh && gunicorn solarvillage.wsgi:application --bind 0.0.0.0:80
