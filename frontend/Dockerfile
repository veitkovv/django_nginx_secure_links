# The instructions for the first stage
FROM node:10-alpine as builder

ARG NODE_ENV=development
ENV NODE_ENV=${NODE_ENV}

COPY package*.json ./

RUN npm install

# The instructions for second stage
FROM node:10-alpine

WORKDIR /opt/services/django_nginx_secure_link/frontend

COPY --from=builder node_modules node_modules

ADD . .

CMD [ "npm", "run", "serve" ]