from django.contrib import admin
from .models import Category, Question, Choice, ExamConfig, QuestionParameter


@admin.register(ExamConfig)
class ExamConfigAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'year', 'num_choices', 'time_limit']
    fieldsets = [
        ('ข้อมูลรายวิชา', {'fields': ['subject_name', 'year', 'num_choices', 'time_limit']}),
        ('Background Images (URL จาก Unsplash หรืออื่นๆ)', {'fields': [
            'home_bg', 'student_login_bg', 'teacher_login_bg',
            'student_register_bg', 'teacher_register_bg', 'exam_bg'
        ]}),
    ]

    def has_add_permission(self, request):
        return not ExamConfig.objects.exists()


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    fields = ['number', 'body']


class QuestionParameterInline(admin.StackedInline):
    model = QuestionParameter
    extra = 0
    fields = ['correct_answer', 'difficulty', 'param_a', 'param_c']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['number', 'category', 'stem_preview', 'get_correct_answer', 'get_difficulty', 'is_active']
    list_editable = ['is_active']
    search_fields = ['body', 'stem', 'number']
    list_filter = ['category', 'is_active']
    inlines = [ChoiceInline, QuestionParameterInline]

    def stem_preview(self, obj):
        return (obj.stem or obj.body)[:80]
    stem_preview.short_description = 'คำถาม'

    def get_correct_answer(self, obj):
        p = getattr(obj, 'parameter', None)
        return p.correct_answer if p else '-'
    get_correct_answer.short_description = 'เฉลย'

    def get_difficulty(self, obj):
        p = getattr(obj, 'parameter', None)
        return p.difficulty if p else '-'
    get_difficulty.short_description = 'ความยาก'


@admin.register(QuestionParameter)
class QuestionParameterAdmin(admin.ModelAdmin):
    list_display = ['question', 'correct_answer', 'difficulty', 'param_a', 'param_c']
    search_fields = ['question__number']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'number', 'body']
    list_filter = ['number']
    search_fields = ['body', 'question__number']
