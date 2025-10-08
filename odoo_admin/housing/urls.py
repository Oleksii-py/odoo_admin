from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, AccommodationViewSet, HousingAssignmentViewSet

routers = DefaultRouter()
routers.register(r"accomodations", AccommodationViewSet, basename="accommodation")
routers.register(r"rooms", RoomViewSet, basename="room")
routers.register(r"housing_assignments", HousingAssignmentViewSet)
urlpatterns = routers.urls
