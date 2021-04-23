from unittest.mock import patch, MagicMock

from django.conf import settings
from django.test import TestCase
from freezegun import freeze_time

from app.services.weather import get_weather, filter_visits, filter_hottest
from tests.data.weather import sample_response


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, data):
            self.data = data

        def json(self):
            return self.data

    return MockResponse(sample_response["TORONTO"])


class WeatherTestCase(TestCase):
    @patch("app.services.weather.requests.get", side_effect=mocked_requests_get)
    @patch("app.services.weather.get_geocode_limiter")
    @patch("app.services.weather.cache")
    @patch("app.services.weather.Location")
    def test_successful_get_weather(
        self, location, cache, get_geocode_limiter, requests
    ):
        test_city = "Toronto"
        cache.get.return_value = None
        requests.return_value.json.return_value = sample_response[test_city.upper()]

        responses = get_weather([test_city])

        self.assertEqual(responses, sample_response)

        cache.get.assert_called_once()
        cache.set.assert_called_once()
        get_geocode_limiter.assert_called_once()
        requests.assert_called_once()
        location.objects.filter.assert_called_once()
        location.objects.bulk_create.assert_called_once()

    def test_successful_filter_visits(self):
        filtered_responses = filter_visits(
            sample_response, weather="Clouds", day_difference=1
        )
        self.assertEqual(filtered_responses, {"TORONTO": "2021-04-23T17:00:00"})

    def test_successful_filter_visits_not_found(self):
        filtered_responses = filter_visits(
            sample_response, weather="Sunny", day_difference=1
        )
        self.assertEqual(filtered_responses, {})

    def test_successful_filter_hottest(self):
        filtered_responses = filter_hottest(sample_response, day_difference=1)
        self.assertEqual(filtered_responses, {"TORONTO": 14.82})
