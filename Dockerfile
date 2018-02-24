FROM python:2.7

MAINTAINER Kevin Yu <bbcyyb@gmail.com>

ENV NGINX_VERSION 1.9.11-1~jessie

# ENV NGINX_MAX_UPLOAD 1m
ENV NGINX_MAX_UPLOAD 0

ENV NGINX_WORKER_PROCESSES 1

ENV LISTEN_PORT 80

ENV PRE_START_PATH /conf/prestart.sh

RUN pip install uwsgi \
    && apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
    && echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y ca-certificates nginx=${NGINX_VERSION} gettext-base \
    && apt-get install -y supervisor \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log \
    && echo "daemon off;" >> /etc/nginx/nginx.conf \
    && rm /etc/nginx/conf.d/default.conf

COPY ./bin/uwsgi.ini /etc/uwsgi/

COPY ./bin/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY requirements.txt /conf/requirements.txt

COPY ./bin/prestart.sh /conf/prestart.sh

RUN pip install -r /conf/requirements.txt

EXPOSE 80 443


COPY ./bin/entrypoint.sh /conf/entrypoint.sh

RUN chmod +x /conf/entrypoint.sh

COPY ./app /app

WORKDIR /app

ENTRYPOINT ["/conf/entrypoint.sh"]

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
