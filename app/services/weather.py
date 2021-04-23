import requests

from datetime import datetime, timedelta

from django.conf import settings
from django.core.cache import cache

from app.services.geocode import get_geocode_limiter
from app.contrib.locations.models import Location


def get_weather(cities):
    cities = [city.upper() for city in cities]
    db_locations = Location.objects.filter(name__in=cities)
    for db_location in db_locations:
        cities.remove(db_location.name)

    locations_by_city = {
        _.name: {"latitude": _.latitude, "longitude": _.longitude} for _ in db_locations
    }
    if cities:
        geocode = get_geocode_limiter()
        locations = {city: geocode(city) for city in cities}
        location_objs = []
        for city, location in locations.items():
            locations_by_city[city] = {
                "latitude": location.latitude,
                "longitude": location.longitude,
            }
            location_objs.append(
                Location(
                    name=city, latitude=location.latitude, longitude=location.longitude
                )
            )
        Location.objects.bulk_create(location_objs)

    responses = {}
    for city, location in locations_by_city.items():
        response = cache.get(city)
        if not response:
            response = requests.get(
                settings.OPENWEATHERMAP_API_URL,
                params={
                    "lat": location.get("latitude"),
                    "lon": location.get("longitude"),
                    "exclude": ",".join(settings.OPENWEATHERMAP_EXCLUDE),
                    "units": settings.OPENWEATHERMAP_UNITS,
                    "appid": settings.OPENWEATHERMAP_API_KEY,
                },
            ).json()
            cache.set(city, response, timeout=settings.CACHE_TTL)
        responses[city] = response

    return responses


def filter_visits(responses, weather, day_difference):
    filtered_responses = {}

    for city, response in responses.items():
        daily = response.get("daily", [])
        first_ts = daily[0].get("dt")
        target_date = datetime.fromtimestamp(first_ts) + timedelta(days=day_difference)
        target_ts = target_date.timestamp()

        target_day = [day for day in daily if day.get("dt") == target_ts]
        if not target_day:
            continue

        target_weather = [
            _
            for _ in target_day[0].get("weather")
            if _.get("main").upper() == weather.upper()
        ]
        if not target_weather:
            continue

        filtered_responses[city] = target_date.strftime("%Y-%m-%dT%H:%M:%S%z")

    return filtered_responses


def filter_hottest(responses, day_difference):
    filtered_responses = []

    for city, response in responses.items():
        daily = response.get("daily", [])
        first_ts = daily[0].get("dt")
        target_date = datetime.fromtimestamp(first_ts) + timedelta(days=day_difference)
        target_ts = target_date.timestamp()

        target_day = [day for day in daily if day.get("dt") == target_ts]
        if not target_day:
            continue

        filtered_responses.append((city, target_day[0].get("temp", {}).get("max")))

    hottest_cities = sorted(filtered_responses, key=lambda x: x[1], reverse=True)
    return dict(hottest_cities[:3])