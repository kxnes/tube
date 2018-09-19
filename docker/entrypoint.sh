#!/usr/bin/env bash

set -e

wait_for_service() {
    python ${PWD}/docker/wait_for_service.py "$1"
}

configure_local_settings() {
    cp ${PWD}/src/settings/local.example.py ${PWD}/src/settings/local.py
    sed -i "
        s|--DB_NAME--|${DB_NAME}|
        s|--DB_HOST--|${DB_HOST}|
        s|--DB_PORT--|${DB_PORT}|
        s|--DB_USER--|${DB_USER}|
        s|--DB_PASSWORD--|${DB_PASSWORD}|

        s|--REDIS_HOST--|${REDIS_HOST}|
        s|--REDIS_PORT--|${REDIS_PORT}|
        s|--REDIS_DB--|${REDIS_DB}|

        s|--YOUTUBE_API_KEY--|${YOUTUBE_API_KEY}|;" ${PWD}/src/settings/local.py
}

migrate() {
    python ${PWD}/manage.py migrate --database default
}

create_admin() {
    python ${PWD}/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" &> /dev/null || true
}

run_server() {
    configure_local_settings
    wait_for_service db
    migrate
    create_admin
    python ${PWD}/manage.py runserver 0.0.0.0:8000
}

run_worker() {
    configure_local_settings
    wait_for_service db
    wait_for_service redis
    wait_for_service server
    celery -A src.app beat --detach
    celery -A src.app worker
}

case "$1" in
    -s | --server) run_server;;
    -c | --worker) run_worker;;
    *)             exec "$@";;
esac
