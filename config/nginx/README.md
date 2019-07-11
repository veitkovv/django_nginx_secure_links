Настройка контейнера nginx.

NGINX выполняет важную работу в приложении:
 1) Раздает файлы из папки /secure, контролируя валидность сгенерированной ссылки, используя модуль secure_link
 2) Дает авторизацию SSO в домене MS AD, если правильно приготовить настройки. 
 
Что можно редактировать в "nginx.vh.default.conf" (nginx.conf не для редактирования):

    location /secure {
        autoindex off;
        alias /opt/services/django_nginx_secure_link/secure/;
        secure_link $arg_md5,$arg_expires;
        secure_link_md5 "mLErOVGhYuM7$uri$secure_link_expires"; - здесь необходимо задать пароль для вычисления md5 (первый параметр), такой же должен быть в django settings
        if ($secure_link = "") { return 403; }
        if ($secure_link = "0") { return 410; }
    }
    
    Далее идут настройки для SSO
    # Here kerberos stuff starts
    auth_gss     on;
    auth_gss_realm DOMAIN.LOCAL;
    #Keytab file from the mounted folder
    auth_gss_keytab /home/spnego/config/web.keytab;
    auth_gss_service_name HTTP/HOST-LINUX.domain.local;
    auth_gss_allow_basic_fallback off;
    #Here kerberos stuff ends
    
Я ссылался на статью на хабре https://habr.com/ru/post/419975/ при настройке SSO, там же описывается как сгенерировать keytab
