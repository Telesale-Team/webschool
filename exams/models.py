from django.db import models
from accounts.models import Student
from questions.models import Question


class ExamSession(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    abandoned_at = models.DateTimeField(null=True, blank=True)
    question_order = models.JSONField(default=list)  # list of question IDs in random order
    current_index = models.IntegerField(default=0)
    time_limit_seconds = models.IntegerField(default=0)  # copy จาก ExamConfig ตอนสร้าง session

    def __str__(self): return f"{self.student} - {self.started_at.date()}"

    class Meta:
        verbose_name = 'เซสชันสอบ'
        verbose_name_plural = 'เซสชันสอบ'


class StudentAnswer(models.Model):
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=10)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['session', 'question']
