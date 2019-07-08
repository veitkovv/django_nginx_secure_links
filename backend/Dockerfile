FROM python:alpine

RUN mkdir -p /opt/services/django_nginx_secure_link
WORKDIR /opt/services/django_nginx_secure_link

ADD . /opt/services/django_nginx_secure_link

RUN \
 apk add --no-cache openldap-dev && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


RUN pip install --upgrade pip
RUN python manage.py collectstatic --no-input

EXPOSE 8000
CMD ["gunicorn", "--chdir", "backend", "--bind", ":8000", "backend.wsgi:application", "--reload"]
