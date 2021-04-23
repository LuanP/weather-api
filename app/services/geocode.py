from django.conf import settings

from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim


def get_geocode_limiter():
    geolocator = Nominatim(user_agent=settings.APP_NAME)
    return RateLimiter(geolocator.geocode, min_delay_seconds=1)