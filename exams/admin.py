from django.contrib import admin
from .models import ExamSession, StudentAnswer


class AnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0
    readonly_fields = ['question', 'answer', 'answered_at']


@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ['student', 'started_at', 'finished_at', 'current_index']
    list_filter = ['finished_at']
    inlines = [AnswerInline]
