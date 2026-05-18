from django.core.management.base import BaseCommand
from questions.models import Question, QuestionParameter
import openpyxl

class Command(BaseCommand):
    help = 'Import answers and difficulty from Excel into QuestionParameter'

    def add_arguments(self, parser):
        parser.add_argument('excel_path', type=str)

    def handle(self, *args, **options):
        wb = openpyxl.load_workbook(options['excel_path'])
        ws = wb.active
        updated = 0
        not_found = 0

        for row in ws.iter_rows(min_row=2, values_only=True):
            # Col A=ข้อ, B=param_a, C=difficulty(b), D=param_c, E=เฉลย
            if not row[0]:
                continue
            try:
                q_number = int(row[0])
                param_a = float(row[1]) if row[1] is not None else None
                difficulty = float(row[2]) if row[2] is not None else None
                param_c = float(row[3]) if row[3] is not None else None
                correct_answer = str(int(row[4])) if row[4] is not None else ''

                try:
                    q = Question.objects.get(number=q_number)
                    param, _ = QuestionParameter.objects.get_or_create(question=q)
                    param.param_a = param_a
                    param.difficulty = difficulty
                    param.param_c = param_c
                    param.correct_answer = correct_answer
                    param.save()
                    updated += 1
                except Question.DoesNotExist:
                    not_found += 1
            except (ValueError, TypeError) as e:
                self.stdout.write(f'Skip row {row[0]}: {e}')

        self.stdout.write(self.style.SUCCESS(
            f'Updated {updated} QuestionParameter records, not found: {not_found}'
        ))
