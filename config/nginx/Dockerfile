FROM alpine:latest

ENV NGINX_VERSION 1.17.1

RUN set -ex \
  && apk add --no-cache \
    git \
    krb5 \
    krb5-dev \
    ca-certificates \
    libressl \
    pcre \
    zlib \
  && apk add --no-cache --virtual .build-deps \
    build-base \
    linux-headers \
    libressl-dev \
    pcre-dev \
    wget \
    zlib-dev \
  && cd /tmp \
  && wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz \
  && tar xzf nginx-${NGINX_VERSION}.tar.gz \
  && git clone https://github.com/stnoonan/spnego-http-auth-nginx-module.git nginx-${NGINX_VERSION}/spnego-http-auth-nginx-module


RUN cd /tmp/nginx-${NGINX_VERSION} \
  && ./configure \
    \
    --prefix=/etc/nginx \
    --sbin-path=/usr/sbin/nginx \
    --conf-path=/etc/nginx/nginx.conf \
    --error-log-path=/var/log/nginx/error.log \
    --pid-path=/var/run/nginx.pid \
    --lock-path=/var/run/nginx.lock \
    --user=nginx \
    --group=nginx \
    --with-threads \
    --with-file-aio \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_auth_request_module \
    --with-http_random_index_module \
    --with-http_secure_link_module \
    --with-http_slice_module \
    --with-http_stub_status_module \
    --http-log-path=/var/log/nginx/access.log \
    --http-client-body-temp-path=/var/cache/nginx/client_temp \
    --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
    --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
    --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
    --http-scgi-temp-path=/var/cache/nginx/scgi_temp \
    --with-mail \
    --with-mail_ssl_module \
    --with-stream \
    --with-stream_ssl_module \
    --with-stream_realip_module \
    --add-module=spnego-http-auth-nginx-module \
  && make -j$(getconf _NPROCESSORS_ONLN) \
  && make install \
  && adduser -D nginx \
  && mkdir -p /var/cache/nginx \
  && apk del .build-deps \
  && rm -rf /tmp/* \
  # forward request and error logs to docker log collector
  && ln -sf /dev/stdout /var/log/nginx/access.log \
  && ln -sf /dev/stderr /var/log/nginx/error.log

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.vh.default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443

STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]
