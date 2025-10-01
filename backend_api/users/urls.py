from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, LogoutView, ForgotPasswordView, ResetPasswordView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

app_name = 'v1'

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # JWT Authentication endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    # Password reset endpoints
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset_password'),

    # User management endpoints
    path('', include(router.urls)),
]

