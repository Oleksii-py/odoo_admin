from rest_framework.routers import DefaultRouter
from .views import WorkPlaceViewSet, WorkPositionViewSet

routers = DefaultRouter()
routers.register(r"workplaces", WorkPlaceViewSet)
routers.register(r"workpositions", WorkPositionViewSet)
urlpatterns = routers.urls
