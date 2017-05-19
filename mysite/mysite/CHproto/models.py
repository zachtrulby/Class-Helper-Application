from django.contrib.auth.models import User
from django.db import models
import datetime

class Course(models.Model):
    def __str__(self):
        return self.name
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    hrs_per_mtg = models.IntegerField()
    mtgs_per_week = models.IntegerField()

class Student(models.Model):
    def __str__(self):
        return(self.first_name + " " + self.last_name)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    student_id_num = models.IntegerField(unique=True)
    email = models.CharField(max_length=200)
    major = models.CharField(max_length=200)
    grad_year = models.IntegerField()

class Roster(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return(self.course.name + ": " + self.student.first_name + " " + self.student.last_name)


class Attendance(models.Model):

    #teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    #course = models.ForeignKey(Course, on_delete=models.CASCADE)
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE, null=True)

    date = models.DateField()
    week_number = models.IntegerField()
    month_number = models.IntegerField()
    ATTENDANCE_MARK_CHOICES = (
        ('FULL', 'FULL'),
        ('TARDY', 'TARDY'),
        ('ABSENT', 'ABSENT'),
    )
    attendance_mark = models.CharField(max_length=8, choices=ATTENDANCE_MARK_CHOICES)
    hours_attended = models.IntegerField()
    absent_excused = models.NullBooleanField()
    tardy_reason = models.CharField(max_length=200, null=True, blank=True)
