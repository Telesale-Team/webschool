import os, sys, io
os.environ['DJANGO_SETTINGS_MODULE'] = 'exam_system.settings'

import django
django.setup()

from django.core.management import call_command

buf = io.StringIO()
call_command('dumpdata', 'accounts', 'questions', 'exams', indent=2, stdout=buf)

with open('fixture_data.json', 'w', encoding='utf-8') as f:
    f.write(buf.getvalue())

print(f"Exported {len(buf.getvalue())} chars to fixture_data.json")
