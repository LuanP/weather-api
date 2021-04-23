#!/bin/sh

compose="docker-compose -f ./docker/docker-compose.yml"

$compose down $@
