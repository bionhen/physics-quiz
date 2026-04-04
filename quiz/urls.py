from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('questions/', views.question_list, name='question_list'),
    path('add/', views.add_question, name='add_question'),
    path('quiz/', views.quiz_view, name='quiz'),
]