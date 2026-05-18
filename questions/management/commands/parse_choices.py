import re
from django.core.management.base import BaseCommand
from questions.models import Question, Choice


def parse_question_body(body):
    """
    แยก stem (คำถาม) และ choices (ตัวเลือก 1-5) ออกจาก body ที่ได้จาก docx
    Returns: (stem: str, choices: dict {1: text, 2: text, ...})
    """
    # ตัดเลขข้อออกจากต้น เช่น "1.คำถาม..." → "คำถาม..."
    body_clean = re.sub(r'^\d+\.\s*', '', body.strip())

    # หาตำแหน่งที่ตัวเลือกเริ่ม
    # pattern: "1." ตามด้วยข้อความ จากนั้นมี "2." "3." "4." ตามมา
    # ต้องเจอ 1. อยู่ก่อน 2. เสมอ
    choice_start = None
    pattern = re.compile(r'(?:^|\n|\t|\s{2,})(1)\.\s', re.MULTILINE)

    for m in pattern.finditer(body_clean):
        rest = body_clean[m.start():]
        # ตรวจว่าหลัง "1." มี "2." และ "3." ด้วย
        if re.search(r'2\.\s', rest) and re.search(r'3\.\s', rest):
            choice_start = m.start()
            break

    if choice_start is None:
        # ไม่พบตัวเลือก — ใช้ body ทั้งหมดเป็น stem
        return body_clean.strip(), {}

    stem = body_clean[:choice_start].strip()
    choice_block = body_clean[choice_start:].strip()

    # แยกแต่ละตัวเลือก: หา "1." "2." ... "5." ตามลำดับ
    markers = list(re.finditer(r'(?:^|\s)([1-5])\.\s+', choice_block, re.MULTILINE))

    choices = {}
    for i, m in enumerate(markers):
        num = int(m.group(1))
        start = m.end()
        end = markers[i + 1].start() if i + 1 < len(markers) else len(choice_block)
        text = choice_block[start:end].strip()
        text = re.sub(r'\s+', ' ', text).strip()  # compact whitespace
        choices[num] = text

    return stem, choices


class Command(BaseCommand):
    help = 'Parse stem and choices from question body and store in DB'

    def handle(self, *args, **options):
        questions = Question.objects.prefetch_related('choices').all()
        parsed = 0
        no_choices = 0

        for q in questions:
            stem, choices = parse_question_body(q.body)
            q.stem = stem
            q.save(update_fields=['stem'])

            # ลบ choices เก่าแล้วสร้างใหม่
            q.choices.all().delete()

            if choices:
                Choice.objects.bulk_create([
                    Choice(question=q, number=num, body=text)
                    for num, text in choices.items()
                ])
                parsed += 1
            else:
                # ไม่มี choices — สร้าง placeholder 1-5 ว่างเปล่า
                Choice.objects.bulk_create([
                    Choice(question=q, number=n, body='')
                    for n in range(1, 6)
                ])
                no_choices += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done: {parsed} questions parsed with choices, '
            f'{no_choices} questions had no parseable choices (placeholders created)'
        ))
