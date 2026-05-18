from django.urls import path
from . import views

app_name = 'questions'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('questions/', views.question_list, name='question_list'),
    path('questions/<int:pk>/edit/', views.edit_question, name='edit_question'),
    path('settings/', views.settings_view, name='settings'),
    path('profile/', views.profile_view, name='profile'),
    path('reports/', views.report_view, name='reports'),
    path('reports/export/excel/', views.export_excel, name='export_excel'),
    path('reports/export/pdf/', views.export_pdf, name='export_pdf'),
    path('questions/export/', views.export_questions, name='export_questions'),
    path('students/export/', views.export_students, name='export_students'),
]
