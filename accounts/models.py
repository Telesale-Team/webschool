from django.db import models
from django.contrib.auth.hashers import make_password, check_password as _check


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, verbose_name='เลขประจำตัวนักเรียน')
    first_name = models.CharField(max_length=100, verbose_name='ชื่อ')
    last_name = models.CharField(max_length=100, verbose_name='นามสกุล')
    phone = models.CharField(max_length=15, verbose_name='เบอร์โทรศัพท์')
    grade = models.CharField(max_length=20, verbose_name='ชั้นปี')
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw): self.password_hash = make_password(raw)
    def check_password(self, raw): return _check(raw, self.password_hash)
    def __str__(self): return f"{self.first_name} {self.last_name} ({self.student_id})"

    class Meta:
        verbose_name = 'นักเรียน'
        verbose_name_plural = 'นักเรียน'


class Teacher(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='ชื่อ')
    last_name = models.CharField(max_length=100, verbose_name='นามสกุล')
    phone = models.CharField(max_length=15, unique=True, verbose_name='เบอร์โทรศัพท์')
    subject = models.CharField(max_length=100, verbose_name='วิชาที่สอน')
    password_hash = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default='', verbose_name='อีเมล')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='รูปโปรไฟล์')
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw): self.password_hash = make_password(raw)
    def check_password(self, raw): return _check(raw, self.password_hash)
    def __str__(self): return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'ครู'
        verbose_name_plural = 'ครู'
