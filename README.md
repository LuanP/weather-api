# Weather API

## Prerequisites

- Docker

**NOTE:** Substitute the value in `OPENWEATHERMAP_API_KEY` in `docker/docker-compose.yml` with your API key from `https://openweathermap.org/api` or add your API key when running the command `OPENWEATHERMAP_API_KEY=your-api-key ./scripts/start.sh`

## Usage

Run `./scripts/start.sh`

To stop the containers, run `./scripts/stop.sh` (this will do a `docker-compose down`), if you wish to also remove the volumes, include a `-v` flag in the command: `./scripts/stop.sh -v`

Example checking:

- `Rain` weather in `2 days` from now in `Toronto, Montreal, Quebec, Vancouver`
- Hottest 3 cities between `Calgary, Toronto, Montreal, Quebec, Vancouver` in `1 day` from now

```shell
curl --location --request POST 'http://localhost:8000/graphql' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=B9JeqTlDDGHDzUgO6ad1v7jEWrehg1zx0aCvLOkrp9pA8NiTy9FMOem34wo64EYn' \
--data-raw '{"query":"query {\n  visits(cities: [\"Toronto\", \"Montreal\", \"Quebec\", \"Vancouver\"], weather: \"Rain\", dayDifference: 2) {\n    city\n    targetDate\n  }\n  hottest(cities: [\"Toronto\", \"Montreal\", \"Quebec\", \"Vancouver\", \"Calgary\"], dayDifference: 1) {\n    city\n    maxTemperature\n  }\n}","variables":{}}'
```

Example response:

```json
{
  "data": {
    "visits": [
      {
        "city": "VANCOUVER",
        "targetDate": "2021-04-23T20:00:00"
      }
    ],
    "hottest": [
      {
        "city": "TORONTO",
        "maxTemperature": 16.59
      },
      {
        "city": "VANCOUVER",
        "maxTemperature": 15.03
      },
      {
        "city": "MONTREAL",
        "maxTemperature": 13.52
      }
    ]
  }
}
```

## Running the API locally (outside Docker)

In order to run the API locally (without docker) it's also required to have:

- pipenv
- Python 3.9 (suggested to use `pyenv`)

Run `./scripts/start.sh db redis` to spin up Postgres and Redis

Create a `.env` file and add:

```shell
OPENWEATHERMAP_API_KEY=your-api-key
SECRET_KEY=django-insecure-cbr1p&$zn9jd()-f*%3c44(o=mmyy5i(tsis6v0%@stix4b=bg
DEBUG="True"
ALLOWED_HOSTS=*

# Postgres
WEATHER_DB_NAME=weather-db
WEATHER_DB_USERNAME=weather-db
WEATHER_DB_PASSWORD=weather-db
WEATHER_DB_HOST=localhost
WEATHER_DB_PORT=5431

# Redis Cache
CACHE_LOCATION=redis://127.0.0.1:6378/1
```

Then, run:

1. pipenv install
2. pipenv run ./manage.py runserver

## Runnings tests

1. pipenv install --dev
2. ./scripts/test.sh

## TODO

1. Error handling on API Endpoint inputs (city, weather, day difference)
2. Increase test coverage
3. Improve README to abide to `standard-readme`
4. Add git hooks with `pre-commit` to include linting, security checks and unit test execution
5. Add RESTful endpoints using django DRF including documentation with API Blueprint
