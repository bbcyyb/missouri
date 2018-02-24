#!/usr/bin/env bash
set -e

USE_NGINX_MAX_UPLOAD=${NGINX_MAX_UPLOAD:-0}

echo "client_max_body_size ${USE_NGINX_MAX_UPLOAD};" > /etc/nginx/conf.d/upload.conf

USE_STATIC_URL=${USE_STATIC_URL:-'/static'}
USE_STATIC_PATH=${USE_STATIC_PATH:-'/src/static'}
USE_LISTEN_PORT=${USE_LISTEN_PORT:-80}
PRE_START_PATH=$P{PRE_START_PATH:-'/conf/prestart.sh'}

echo "server {
    listen ${USE_LISTEN_PORT};
    location / {
        try_files \$uri @src;
    }
    location @src {
        include uwsgi_params;
        uwsgi_pass unix:///tmp/uwsgi.sock;
    }
    location ${USE_STATIC_URL} {
        alias ${USE_STATIC_PATH};
    }" > /etc/nginx/conf.d/nginx.conf

if [[ ${STATIC_INDEX} == 1 ]]; then
echo "  location = / {
        index ${USE_STATIC_URL}/index.html;
    }" >> /etc/nginx/conf.d/nginx.conf
fi

echo "}" >> /etc/nginx/conf.d/nginx.conf

echo "** Checking for script in ${PRE_START_PATH}"
if [[ -f ${PRE_START_PATH} ]]; then
    echo "** Running script ${PRE_START_PATH}"
    source ${PRE_START_PATH}
else
    echo "** There is no script ${PRE_START_PATH}"
fi

exec "$@"
