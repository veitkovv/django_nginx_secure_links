# The instructions for the first stage
FROM node:alpine as builder

ARG NODE_ENV=development
ENV NODE_ENV=${NODE_ENV}

COPY package*.json ./

RUN npm install

# The instructions for second stage
FROM node:alpine

WORKDIR /opt/services/django_nginx_secure_link/frontend

COPY --from=builder node_modules node_modules

ADD . .

RUN npm run build

CMD if [ "$MODE" = "dev" ] ; then npm run serve ; echo "running production saticfiles serving" ; fi