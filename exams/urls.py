from django.urls import path
from . import views

app_name = 'exams'
urlpatterns = [
    path('question/', views.question_view, name='question'),
    path('finished/', views.finished_view, name='finished'),
]
