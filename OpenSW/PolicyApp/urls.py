from django.urls import path
from .views import *
from . import views

app_name="PolicyApp"
urlpatterns = [
    path('', views.policy_list_create),
]
