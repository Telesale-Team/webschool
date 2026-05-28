import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')

import django
django.setup()
from questions.models import Question, Choice

problem_numbers = [40,45,48,55,61,62,65,70,72,77,85,89,94,97,98,100,109,117,123,142]

for db_num in problem_numbers:
    try:
        q = Question.objects.get(number=db_num)
    except Exception:
        print(f'Q{db_num}: NOT IN DB')
        continue
    choices_list = list(q.choices.all())
    empty = [c.number for c in choices_list if not c.body.strip()]
    print(f'Q{db_num}: correct={q.correct_answer}, empty_choices={empty}')
    for c in sorted(choices_list, key=lambda x: x.number):
        marker = '<EMPTY>' if not c.body.strip() else ''
        print(f'  [{c.number}]: {repr(c.body[:60])} {marker}')
