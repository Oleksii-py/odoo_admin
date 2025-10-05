from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, AccommodationViewSet

routers = DefaultRouter()
routers.register(r"accomodations", AccommodationViewSet)
routers.register(r"rooms", RoomViewSet)
urlpatterns = routers.urls
