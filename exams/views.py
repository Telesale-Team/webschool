from django.shortcuts import render, redirect
from django.utils import timezone
from .models import ExamSession, StudentAnswer
from questions.models import Question, ExamConfig
from accounts.models import Student


def question_view(request):
    if not request.session.get('student_id'):
        return redirect('accounts:student_login')

    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        request.session.flush()
        return redirect('accounts:student_login')
    session = ExamSession.objects.filter(
        student=student,
        finished_at__isnull=True,
        abandoned_at__isnull=True
    ).first()

    if not session:
        config = ExamConfig.get()

        # ข้อที่เคยตอบแล้ว
        if config.allow_retake:
            answered_ids = set()
        else:
            answered_ids = set(
                StudentAnswer.objects.filter(session__student=student)
                .values_list('question_id', flat=True)
            )

        # queryset
        qs = Question.objects.filter(is_active=True).exclude(id__in=answered_ids)

        # ลำดับ
        if config.question_order == 'difficulty':
            qs = qs.order_by('parameter__difficulty', 'number')
        elif config.question_order == 'random':
            qs = qs.order_by('?')
        else:  # sequential
            qs = qs.order_by('number')

        question_ids = list(qs.values_list('id', flat=True))

        # จำกัดจำนวนข้อ
        if config.questions_per_session > 0:
            question_ids = question_ids[:config.questions_per_session]

        session = ExamSession.objects.create(
            student=student,
            question_order=question_ids,
            time_limit_seconds=config.time_limit,
        )

    if session.current_index >= len(session.question_order):
        session.finished_at = timezone.now()
        session.save()
        return redirect('exams:finished')

    if request.method == 'POST':
        q_id = session.question_order[session.current_index]
        question = Question.objects.get(id=q_id)
        answer = request.POST.get('answer', '')
        StudentAnswer.objects.get_or_create(session=session, question=question, defaults={'answer': answer})
        session.current_index += 1
        session.save()
        return redirect('exams:question')

    q_id = session.question_order[session.current_index]
    question = Question.objects.prefetch_related('choices').get(id=q_id)
    total = len(session.question_order)
    config = ExamConfig.get()
    elapsed = int((timezone.now() - session.started_at).total_seconds())
    return render(request, 'exams/question.html', {
        'question': question,
        'choices': question.choices.all(),
        'current': session.current_index + 1,
        'total': total,
        'student': student,
        'progress_pct': int((session.current_index / total) * 100),
        'config': config,
        'time_limit': session.time_limit_seconds,
        'elapsed_seconds': elapsed,
    })


def finished_view(request):
    if not request.session.get('student_id'):
        return redirect('accounts:student_login')
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        request.session.flush()
        return redirect('accounts:student_login')
    return render(request, 'exams/finished.html', {'student': student})
