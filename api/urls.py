from django.urls import path
from api import views

urlpatterns = [
    path('register/', views.UserCreatView.as_view()),
]