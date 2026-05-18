from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentRegisterForm, TeacherRegisterForm, StudentLoginForm, TeacherLoginForm
from .models import Student, Teacher
from questions.models import ExamConfig


def student_register(request):
    form = StudentRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        student = Student(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            student_id=form.cleaned_data['student_id'],
            phone=form.cleaned_data['phone'],
            grade=form.cleaned_data['grade'],
        )
        student.set_password(form.cleaned_data['password'])
        student.save()
        messages.success(request, 'ลงทะเบียนสำเร็จ กรุณาเข้าสู่ระบบ')
        return redirect('accounts:student_login')
    return render(request, 'accounts/student_register.html', {'form': form, 'config': ExamConfig.get()})


def teacher_register(request):
    form = TeacherRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        teacher = Teacher(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            phone=form.cleaned_data['phone'],
            subject=form.cleaned_data['subject'],
        )
        teacher.set_password(form.cleaned_data['password'])
        teacher.save()
        messages.success(request, 'ลงทะเบียนสำเร็จ กรุณาเข้าสู่ระบบ')
        return redirect('accounts:teacher_login')
    return render(request, 'accounts/teacher_register.html', {'form': form, 'config': ExamConfig.get()})


def student_login(request):
    form = StudentLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            student = Student.objects.get(student_id=form.cleaned_data['student_id'])
            if student.check_password(form.cleaned_data['password']):
                request.session['student_id'] = student.id
                request.session['user_type'] = 'student'
                return redirect('exams:question')
        except Student.DoesNotExist:
            pass
        messages.error(request, 'เลขประจำตัวหรือรหัสผ่านไม่ถูกต้อง')
    return render(request, 'accounts/student_login.html', {'form': form, 'config': ExamConfig.get()})


def teacher_login(request):
    form = TeacherLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            teacher = Teacher.objects.get(phone=form.cleaned_data['phone'])
            if teacher.check_password(form.cleaned_data['password']):
                request.session['teacher_id'] = teacher.id
                request.session['user_type'] = 'teacher'
                return redirect('questions:dashboard')
        except Teacher.DoesNotExist:
            pass
        messages.error(request, 'เบอร์โทรหรือรหัสผ่านไม่ถูกต้อง')
    return render(request, 'accounts/teacher_login.html', {'form': form, 'config': ExamConfig.get()})


def logout_view(request):
    student_id = request.session.get('student_id')
    if student_id:
        from exams.models import ExamSession
        from django.utils import timezone
        session = ExamSession.objects.filter(
            student_id=student_id,
            finished_at__isnull=True,
            abandoned_at__isnull=True
        ).first()
        if session:
            session.abandoned_at = timezone.now()
            session.save(update_fields=['abandoned_at'])
    request.session.flush()
    return redirect('home')
