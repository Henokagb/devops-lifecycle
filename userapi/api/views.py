from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from django.contrib import admin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .modules.validInputs import *
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST, Histogram, Summary
from django.http import HttpResponse


REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
HEALTH_CHECK = Gauge('api_healthcheck', 'Health check status of the API (1=healthy, 0=unhealthy)')
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Latency of HTTP requests', ['endpoint'])
REQUEST_SUMMARY = Summary('http_request_processing_seconds', 'Time spent processing requests')


class UserList(APIView):

    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            "id",
            openapi.IN_QUERY,
            description="User ID",
            type=openapi.TYPE_INTEGER,
            required=False
            ),
        ]
    )
    def get(self, request):
        user_id = request.query_params.get('id')
        if user_id:
            queryset = User.objects.filter(id=user_id)
        else:
            queryset = User.objects.all()
        
        serializer = UserSerializer(queryset, many=True)
        if serializer.data == [] and user_id:
            return Response({"error": "No user found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)


    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if validMail(data['mail']) and validAge(data['age']) and validname(data['name']) and validProfession(data['profession']):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            "id",
            openapi.IN_QUERY,
            description="User ID",
            type=openapi.TYPE_INTEGER,
            required=False
            ),
        ]
    )
    def delete(self, request):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=UserSerializer,
        manual_parameters=[
        openapi.Parameter(
            "id",
            openapi.IN_QUERY,
            description="User ID to update",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
    ]
    )
    def put(self, request):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class Healthcheck(APIView):
    @swagger_auto_schema(
    )
    def get(self, request):
        health_status = True
        HEALTH_CHECK.set(1 if health_status else 0)
        return Response({"HealthCheck": "Healthy" if health_status else "Unhealthy"}, status=status.HTTP_200_OK if health_status else status.HTTP_500_INTERNAL_SERVER_ERROR)

class PrometheusMetrics(APIView):
    @swagger_auto_schema(
    )
    def get(self, request):
        return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)