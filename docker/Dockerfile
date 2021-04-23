FROM python:3.9.4-alpine3.13 AS weather-api

ENV PYTHONUNBUFFERED="1" \
    BUILD_PACKAGES="build-base libffi-dev" \
    POSTGRES_BUILD_PACKAGES="postgresql-dev" \
    POSTGRES_PACKAGES="libpq"

WORKDIR /app

RUN pip install pipenv

COPY Pipfile* .

RUN apk --update add --no-cache --virtual .build-deps \
    ${BUILD_PACKAGES} ${POSTGRES_BUILD_PACKAGES} \
    && apk --update add --no-cache ${POSTGRES_PACKAGES} \
    && pipenv sync --system \
    && apk del --no-cache .build-deps

COPY . .

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
    CMD curl -f http://localhost/ping || exit 1

ENTRYPOINT ["/app/docker/wait-for.sh"]