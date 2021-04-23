#!/bin/sh

# based from: https://github.com/mrts/docker-postgresql-multiple-databases

set -e
set -u

function create_user_and_database() {
    local database=$1
    local username=$2
    local password=$3
    echo "Creating user and database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	    CREATE USER "$username" WITH PASSWORD '$password';
	    CREATE DATABASE "$database";
	    GRANT ALL PRIVILEGES ON DATABASE "$database" TO "$username";
EOSQL
}

create_user_and_database weather-db weather-db $WEATHER_DB_PASSWORD
# create other dbs by simple repeating the row:
# create_user_and_database example-db example-db $EXAMPLE_DB_PASSWORD
