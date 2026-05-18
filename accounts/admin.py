from django.contrib import admin
from .models import Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'grade', 'phone', 'created_at']
    search_fields = ['student_id', 'first_name', 'last_name']
    list_filter = ['grade']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'subject', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone']
