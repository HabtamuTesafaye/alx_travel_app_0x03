from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Travel API",
        default_version='v1',
        description="API documentation for Listings, Bookings, Reviews, and Payments",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # Make Swagger public
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('listings.urls')),             # Main app
    path('api-auth/', include('rest_framework.urls')),  # Browsable login (optional)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger & Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
