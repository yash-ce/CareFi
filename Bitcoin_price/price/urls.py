from django.urls import path

from .views import *

urlpatterns = [
    path('todayprice', price.as_view()),
    path('register/', RegisterUser.as_view()),
    path('', price_list.as_view()),
    
]