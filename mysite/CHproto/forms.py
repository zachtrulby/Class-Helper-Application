from django.forms import ModelForm
from CHproto.models import *
from django import forms

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'student_id_num', 'email', 'major', 'grad_year')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'hrs_per_mtg', 'mtgs_per_week')

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('date', 'attendance_mark', 'absent_excused', 'tardy_reason', 'hours_attended', 'week_number', 'month_number') # 'hours_attended',
