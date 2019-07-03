# The instructions for the first stage
FROM node:latest as builder

ARG NODE_ENV=development
ENV NODE_ENV=${NODE_ENV}

COPY package*.json ./

RUN npm install

# The instructions for second stage
FROM node:latest

WORKDIR /opt/services/django_nginx_secure_link/frontend

COPY --from=builder node_modules node_modules

ADD . .

RUN npm run build

CMD [ "npm", "run", "serve" ]