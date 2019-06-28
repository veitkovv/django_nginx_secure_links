# Django Nginx Secure Links

## О приложении
Приложение реализует веб-интерфейс для функционала [secure link](http://nginx.org/ru/docs/http/ngx_http_secure_link_module.html) веб-сервера nginx с целью быстрого создания защищенных паролем публичных ссылок на файлы и контроля времени жизни ссылки. 
В контейнере nginx собирается веб-сервер nginx из исходников с нужным модулем [secure link](http://nginx.org/ru/docs/http/ngx_http_secure_link_module.html),
в отдельных контейнерах собирается django + node.js + postgreSQL. При необходимости к контейнеру "backend" можно примонтировать уже имеющуюся сетевую папку, и начать раздавать файлы не загружая в облако (мой кейс).

## Используемые технологии 
### Развертывание 
- docker / docker compose

### Backend
- python3.7, django
- postgreSQL
- API GraphQL (graphene, graphene_django)

### Frontend
- vue.js, vuetify
- apollo for GraphQL

## Планы на реализацию
- [ ] SSO MS AD NGINX
- [ ] Автоматическое получение сертификата SSL Letsencrypt
- [ ] Инструкция по запуску
