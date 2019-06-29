from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie
from . import views

urlpatterns = [
    path('csrf/', views.csrf),
]
