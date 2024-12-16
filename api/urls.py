from django.urls import path
from api import views

urlpatterns = [
    path('register/', views.UserCreatView.as_view()),
    path('expenses/', views.ExpenseListCreateView.as_view()),
    path('expenses/<int:pk>/', views.ExpenseRetrieveUpdateDestroyView.as_view()),   
]