import re
from django.core.management.base import BaseCommand
from questions.models import Category, Question
import docx


class Command(BaseCommand):
    help = 'Import questions from .docx file'

    def add_arguments(self, parser):
        parser.add_argument('docx_path', type=str, help='Path to .docx file')

    def handle(self, *args, **options):
        path = options['docx_path']
        doc = docx.Document(path)
        table = doc.tables[0]
        imported = 0
        skipped = 0
        category_cache = {}

        for row in table.rows[2:]:  # skip 2 header rows
            cat_text = row.cells[0].text.strip()
            q_text = row.cells[1].text.strip()
            if not q_text:
                continue

            # Get or create category
            if cat_text not in category_cache:
                cat, _ = Category.objects.get_or_create(name=cat_text)
                category_cache[cat_text] = cat
            category = category_cache[cat_text]

            # Extract question number from start of text
            match = re.match(r'^(\d+)\.', q_text)
            if not match:
                skipped += 1
                continue
            number = int(match.group(1))

            if Question.objects.filter(number=number).exists():
                skipped += 1
                continue

            Question.objects.create(
                category=category,
                number=number,
                body=q_text,
            )
            imported += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {imported} questions, skipped {skipped}'))
