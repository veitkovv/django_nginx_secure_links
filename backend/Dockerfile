FROM python:stretch

ARG MODE
ARG DJANGO_SECRET_KEY
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ARG NGINX_SECRET

ENV MODE=$MODE
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB
ENV NGINX_SECRET=$NGINX_SECRET

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/services/django_nginx_secure_link
WORKDIR /opt/services/django_nginx_secure_link

ADD . /opt/services/django_nginx_secure_link

RUN pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --no-input

EXPOSE 8000
CMD ["gunicorn", "--chdir", "backend", "--bind", ":8000", "backend.wsgi:application", "--reload"]
