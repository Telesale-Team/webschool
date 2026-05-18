from django.db import models


class ExamConfig(models.Model):
    subject_name = models.CharField(max_length=200, default='ระบบสอบออนไลน์', verbose_name='ชื่อรายวิชา')
    year = models.CharField(max_length=10, default='2569', verbose_name='ปีการศึกษา')
    num_choices = models.IntegerField(default=5, verbose_name='จำนวนตัวเลือก (4 หรือ 5)')
    time_limit = models.IntegerField(default=0, verbose_name='เวลาสอบต่อข้อ (วินาที, 0=ไม่จำกัด)')
    home_bg = models.URLField(blank=True, default='', verbose_name='Background หน้า Home (URL)')
    student_login_bg = models.URLField(blank=True, default='', verbose_name='Background นักเรียน Login (URL)')
    teacher_login_bg = models.URLField(blank=True, default='', verbose_name='Background ครู Login (URL)')
    student_register_bg = models.URLField(blank=True, default='', verbose_name='Background นักเรียน Register (URL)')
    teacher_register_bg = models.URLField(blank=True, default='', verbose_name='Background ครู Register (URL)')
    exam_bg = models.URLField(blank=True, default='', verbose_name='Background หน้าข้อสอบ (URL)')
    is_results_published = models.BooleanField(default=False, verbose_name='ประกาศผลการสอบ')
    questions_per_session = models.IntegerField(
        default=0,
        verbose_name='จำนวนข้อต่อครั้ง (0 = ทั้งหมด)'
    )
    question_order = models.CharField(
        max_length=20,
        default='difficulty',
        choices=[
            ('difficulty', 'ง่าย → ยาก (ตาม b-parameter)'),
            ('random', 'สุ่ม'),
            ('sequential', 'ตามลำดับข้อ'),
        ],
        verbose_name='ลำดับข้อสอบ'
    )
    allow_retake = models.BooleanField(
        default=False,
        verbose_name='อนุญาตให้ทำข้อสอบซ้ำ'
    )

    class Meta:
        verbose_name = 'ตั้งค่าการสอบ'
        verbose_name_plural = 'ตั้งค่าการสอบ'

    def __str__(self): return f"{self.subject_name} ({self.year})"

    def save(self, *args, **kwargs):
        self.pk = 1  # singleton
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        config, _ = cls.objects.get_or_create(pk=1, defaults={
            'subject_name': 'ระบบสอบออนไลน์', 'year': '2569', 'num_choices': 5
        })
        return config


class Category(models.Model):
    name = models.TextField(verbose_name='หัวข้อ')

    def __str__(self): return self.name[:60]

    class Meta:
        verbose_name = 'หมวดหมู่'
        verbose_name_plural = 'หมวดหมู่'


class Question(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questions',
        verbose_name='หมวดหมู่'
    )
    number = models.IntegerField(verbose_name='ลำดับข้อ')
    body = models.TextField(verbose_name='โจทย์ (ต้นฉบับ)')
    stem = models.TextField(blank=True, verbose_name='คำถาม (ไม่มีตัวเลือก)')
    image = models.ImageField(upload_to='questions/', blank=True, null=True, verbose_name='รูปภาพประกอบ')
    is_active = models.BooleanField(default=True, verbose_name='เปิดใช้งาน')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def body_clean(self):
        import re
        return re.sub(r'^\d+\.\s*', '', self.body)

    @property
    def correct_answer(self):
        p = getattr(self, 'parameter', None)
        return p.correct_answer if p else ''

    @property
    def difficulty(self):
        p = getattr(self, 'parameter', None)
        return p.difficulty if p else None

    @property
    def param_a(self):
        p = getattr(self, 'parameter', None)
        return p.param_a if p else None

    @property
    def param_c(self):
        p = getattr(self, 'parameter', None)
        return p.param_c if p else None

    def __str__(self): return f"ข้อ {self.number}: {self.body[:50]}"

    class Meta:
        ordering = ['number']
        verbose_name = 'ข้อสอบ'
        verbose_name_plural = 'ข้อสอบ'


class QuestionParameter(models.Model):
    question = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        related_name='parameter',
        verbose_name='ข้อสอบ'
    )
    correct_answer = models.CharField(max_length=10, blank=True, default='', verbose_name='เฉลย')
    difficulty = models.FloatField(null=True, blank=True, verbose_name='ความยาก (b)')
    param_a = models.FloatField(null=True, blank=True, verbose_name='Parameter a')
    param_c = models.FloatField(null=True, blank=True, verbose_name='Parameter c')

    class Meta:
        verbose_name = 'พารามิเตอร์ข้อสอบ'
        verbose_name_plural = 'พารามิเตอร์ข้อสอบ'

    def __str__(self):
        return f"Param ข้อ {self.question.number}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    number = models.IntegerField(verbose_name='ตัวเลือกที่')
    body = models.TextField(blank=True, verbose_name='ข้อความตัวเลือก')

    class Meta:
        ordering = ['number']
        unique_together = ['question', 'number']
        verbose_name = 'ตัวเลือก'
        verbose_name_plural = 'ตัวเลือก'

    def __str__(self): return f"ข้อ {self.question.number} ตัวเลือก {self.number}"
