FROM python:3.13-alpine

WORKDIR /app/

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install gunicorn==23.0.0

COPY . .

RUN python3 manage.py collectstatic --noinput

CMD [ "gunicorn", "solarvillage.wsgi" ]
