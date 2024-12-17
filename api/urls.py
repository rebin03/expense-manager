from django.urls import path
from api import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('register/', views.UserCreatView.as_view()),
    path('expenses/', views.ExpenseListCreateView.as_view()),
    path('expenses/<int:pk>/', views.ExpenseRetrieveUpdateDestroyView.as_view()),
    path('token/', ObtainAuthToken.as_view()), 
]