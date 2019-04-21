FROM node:latest

ADD package.json /tmp/package.json
ADD package-lock.json /tmp/package-lock.json

RUN cd /tmp && npm install

WORKDIR /opt/services/django_nginx_secure_link/frontend

RUN cp -a /tmp/node_modules /opt/services/django_nginx_secure_link/frontend
# From here we load our application's code in, therefore the previous docker
# "layer" thats been cached will be used if possible
ADD . /opt/services/django_nginx_secure_link/frontend
RUN npm run build
ENV PORT=8082
EXPOSE 8082
CMD [ "npm", "run", "serve" ]