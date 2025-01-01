from django.urls import path
from .views import UserList, Healthcheck, PrometheusMetrics
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import os

...

schema_view = get_schema_view(
   openapi.Info(
      title="User API swagger",
      default_version='v1',
      description="test"
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   url = "https://devops-lifecycle.onrender.com/api/" if os.getenv("ENV") == "prod" else None
)

urlpatterns = [
    path('users/', UserList.as_view()),
    path('healthcheck/', Healthcheck.as_view()),
    path('prometheus/', PrometheusMetrics.as_view()),
    path('swagger<format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
