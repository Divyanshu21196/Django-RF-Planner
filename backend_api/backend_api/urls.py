from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)


urlpatterns = [
    #Admin
    path('admin/',admin.site.urls),
    #Api Schema
    path('api/schema/',SpectacularAPIView.as_view(),name='schema'),
    path('api/docs/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('api/redoc/',SpectacularRedocView.as_view(url_name='schema'),name='redoc'),

    #ApiEndpoint
    path('api/',include('users.urls')),
    path('api/',include('stores.urls')),
    path('api/',include('events.urls'))
]
