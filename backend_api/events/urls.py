from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet

app_name = 'v1'

router = DefaultRouter()
router.register(r'events',EventViewSet)

urlpatterns = [
    path('',include(router.urls))
]
