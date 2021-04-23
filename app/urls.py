from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView


def ping(request):
    return HttpResponse("OK")


urlpatterns = [
    path("ping", ping),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=settings.GRAPHIQL))),
]
