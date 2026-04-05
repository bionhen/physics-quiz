from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('questions/', views.question_list, name='question_list'),
    path('add/', views.add_question, name='add_question'),
    path('edit/<int:q_id>/', views.question_edit, name='question_edit'),
    path('delete/<int:q_id>/', views.question_delete, name='question_delete'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.teacher_logout, name='teacher_logout'),
]