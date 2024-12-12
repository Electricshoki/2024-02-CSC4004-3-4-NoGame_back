from django.urls import path
from .views import *
<<<<<<< HEAD
from .views import policy_detail
from . import views

app_name="PolicyApp"

urlpatterns = [
    path('<int:id>/', policy_detail, name='policyidea_detail'),
=======
from . import views

app_name="PolicyApp"
urlpatterns = [
>>>>>>> upstream/main
    path('', views.policy_list_create),
    path('<int:policy_id>/like/', like_policy, name='like_policy'),
    path('<int:policy_id>/scrap/', scrap_policy, name='scrap_policy'),
    path('<int:policy_id>/rate/', rate_policy, name='rate_policy'),
    path('<int:policy_id>/ratings/', list_ratings, name='list_ratings'),
    path('<int:policy_id>/sentiment/', policy_sentiment_analysis, name='policy_sentiment_analysis'),
<<<<<<< HEAD
=======

>>>>>>> upstream/main
]
