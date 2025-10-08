from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import WorkPlaceViewSet, WorkPositionViewSet, AggregationViewSet


urlpatterns = [
    path("aggregation/", AggregationViewSet.as_view(), name="workplace-aggregation"),
]
routers = DefaultRouter()
routers.register(r"workplaces", WorkPlaceViewSet, basename="workplace")
routers.register(r"workpositions", WorkPositionViewSet, basename="workposition")
urlpatterns.extend(routers.urls)
