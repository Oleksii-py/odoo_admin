from rest_framework.routers import DefaultRouter
from .views import WorkerViewSet, NationalityViewSet

routers = DefaultRouter()
routers.register(r"workers", WorkerViewSet)
routers.register(r"nationality", NationalityViewSet)
urlpatterns = routers.urls
