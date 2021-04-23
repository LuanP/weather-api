#!/bin/sh

compose="docker-compose -f ./docker/docker-compose.yml"

WEATHER_DB_HOST=db WEATHER_DB_PORT=5432 \
    $compose up --build --remove-orphans -d $@

$compose logs -f --tail=10 $@
