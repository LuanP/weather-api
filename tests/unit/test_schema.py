from unittest.mock import patch

from graphene_django.utils.testing import GraphQLTestCase

from tests.data.weather import sample_response


class SchemaTestCase(GraphQLTestCase):
    GRAPHQL_URL = "/graphql"

    @patch("app.schema.get_weather")
    def test_filter_visits(self, get_weather):
        get_weather.return_value = sample_response

        response = self.query(
            """
            query visits($cities: [String]!, $weather: String!, $dayDifference: Int!){
                visits(cities: $cities, weather: $weather, dayDifference: $dayDifference) {
                    city
                    targetDate
                }
            }
            """,
            op_name="visits",
            variables={"cities": ["Toronto"], "weather": "Clouds", "dayDifference": 1},
        )

        self.assertResponseNoErrors(response)
        self.assertJSONEqual(
            response.content,
            {
                "data": {
                    "visits": [{"city": "TORONTO", "targetDate": "2021-04-23T17:00:00"}]
                }
            },
        )

    @patch("app.schema.get_weather")
    def test_filter_hottest(self, get_weather):
        get_weather.return_value = sample_response

        response = self.query(
            """
            query hottest($cities: [String]!, $dayDifference: Int!){
                hottest(cities: $cities, dayDifference: $dayDifference) {
                    city
                    maxTemperature
                }
            }
            """,
            op_name="hottest",
            variables={"cities": ["Toronto"], "dayDifference": 1},
        )

        self.assertResponseNoErrors(response)
        self.assertJSONEqual(
            response.content,
            {"data": {"hottest": [{"city": "TORONTO", "maxTemperature": 14.82}]}},
        )