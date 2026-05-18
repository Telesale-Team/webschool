from django import forms
from .models import Student, Teacher


class StudentRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='ชื่อ')
    last_name = forms.CharField(max_length=100, label='นามสกุล')
    student_id = forms.CharField(max_length=20, label='เลขประจำตัวนักเรียน')
    phone = forms.CharField(max_length=15, label='เบอร์โทรศัพท์')
    grade = forms.CharField(max_length=20, label='ชั้นปี')
    password = forms.CharField(widget=forms.PasswordInput, label='รหัสผ่าน')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='ยืนยันรหัสผ่าน')

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError('รหัสผ่านไม่ตรงกัน')
        if Student.objects.filter(student_id=cleaned.get('student_id')).exists():
            raise forms.ValidationError('เลขประจำตัวนักเรียนนี้มีอยู่แล้ว')
        return cleaned


class TeacherRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='ชื่อ')
    last_name = forms.CharField(max_length=100, label='นามสกุล')
    phone = forms.CharField(max_length=15, label='เบอร์โทรศัพท์')
    subject = forms.CharField(max_length=100, label='วิชาที่สอน')
    password = forms.CharField(widget=forms.PasswordInput, label='รหัสผ่าน')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='ยืนยันรหัสผ่าน')

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError('รหัสผ่านไม่ตรงกัน')
        if Teacher.objects.filter(phone=cleaned.get('phone')).exists():
            raise forms.ValidationError('เบอร์โทรศัพท์นี้มีอยู่แล้ว')
        return cleaned


class StudentLoginForm(forms.Form):
    student_id = forms.CharField(max_length=20, label='เลขประจำตัวนักเรียน')
    password = forms.CharField(widget=forms.PasswordInput, label='รหัสผ่าน')


class TeacherLoginForm(forms.Form):
    phone = forms.CharField(max_length=15, label='เบอร์โทรศัพท์')
    password = forms.CharField(widget=forms.PasswordInput, label='รหัสผ่าน')
