import graphene

from app.services.weather import get_weather, filter_visits, filter_hottest


class VisitData(graphene.ObjectType):
    city = graphene.String()
    target_date = graphene.String()


class HottestData(graphene.ObjectType):
    city = graphene.String()
    max_temperature = graphene.Float()


class Query(graphene.ObjectType):
    visits = graphene.List(
        VisitData,
        cities=graphene.List(graphene.String),
        weather=graphene.String(),
        day_difference=graphene.Int(),
    )
    hottest = graphene.List(
        HottestData,
        cities=graphene.List(graphene.String),
        day_difference=graphene.Int(),
    )

    def resolve_visits(root, info, cities, weather, day_difference):
        responses = get_weather(cities)
        filtered_data = filter_visits(responses, weather, day_difference)

        data = []
        for city, target_date in filtered_data.items():
            data.append(VisitData(city=city, target_date=target_date))
        return data

    def resolve_hottest(root, info, cities, day_difference):
        responses = get_weather(cities)
        filtered_data = filter_hottest(responses, day_difference)

        data = []
        for city, max_temperature in filtered_data.items():
            data.append(HottestData(city=city, max_temperature=max_temperature))
        return data


schema = graphene.Schema(query=Query)