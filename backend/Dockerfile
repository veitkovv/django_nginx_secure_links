FROM python:3.7.1-stretch

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/services/django_nginx_secure_link/src
WORKDIR /opt/services/django_nginx_secure_link/src

ADD . /opt/services/django_nginx_secure_link/src

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --no-input

EXPOSE 8000
CMD ["gunicorn", "--chdir", "backend", "--bind", ":8000", "backend.wsgi:application", "--reload"]
