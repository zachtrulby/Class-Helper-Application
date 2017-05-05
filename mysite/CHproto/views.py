from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db import models
from CHproto.models import Course, Student, Roster, Attendance
from django import forms
from django.shortcuts import get_object_or_404
from CHproto.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
"""
def index(request):
    return HttpResponse("Hello, world. You're at the CHproto index.")

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
"""
@login_required
def profile(request):
    user = request.user
    all_user_courses = Course.objects.filter(teacher=user)
    template = loader.get_template('profile.html')
    context = {
        'all_user_courses': all_user_courses,
    }
    return HttpResponse(template.render(context, request))

def register(request):
    if request.method=="POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/CHproto/login')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

@login_required
def roster(request, course_id):
    user = request.user
    curr_course = Course.objects.get(pk=course_id)
    query_results = Roster.objects.filter(course=curr_course) # query_results
    template = loader.get_template('roster.html')
    students = []
    for roster_entry in query_results:
        students.append(Student.objects.get(pk=roster_entry.student.pk))
    context = {
        'students': students,
        'course': curr_course,
    }
    return HttpResponse(template.render(context, request))

@login_required
def newstudent(request, course_id):
    curr_course = Course.objects.get(pk=course_id)
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            user = get_user(request)
            student.teacher = user
            student.save()
            roster_entry = Roster.objects.create(teacher=request.user, course=curr_course, student=student)
            return HttpResponseRedirect('/CHproto/%i/roster/' % curr_course.id)
    else:
        form = StudentForm()
        curr_course = Course.objects.get(pk=course_id)
    context = {
        'course': curr_course,
        'form':form,
    }
    return render(request, 'newstudent.html', context)

@login_required
def editstudent(request, student_id, course_id):
    student = get_object_or_404(Student, pk=student_id)
    curr_course = get_object_or_404(Course, pk=course_id)
    if request.method =="POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return HttpResponseRedirect('/CHproto/%i/roster/' % curr_course.id)
    else:
        form = StudentForm(instance=student)
    return render(request, 'editstudent.html', {'form': form})

@login_required
def removefromroster(request, student_id, course_id):
    curr_student = get_object_or_404(Student, pk=student_id)
    curr_course = get_object_or_404(Course, pk=course_id)

    curr_roster = Roster.objects.filter(student=curr_student, course=curr_course)
    curr_roster.delete()

    return HttpResponseRedirect('/CHproto/%i/roster/' % curr_course.id)


@login_required
def newcourse(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            user = get_user(request)
            new_course.teacher = user
            new_course.save()
            return HttpResponseRedirect('/CHproto/profile')
    else:
        form = CourseForm()

    context = {
        'form':form,
    }

    return render(request, 'newcourse.html', context)

@login_required
def removecourse(request, course_id):
    curr_course = get_object_or_404(Course, pk=course_id)
    curr_course.delete()
    # AND HAVE TO REMOVE ALL ROSTER ENTRIES ASSOCIATED WITH COURSE!!!!!!!
    #######
    #########
    #####

    return HttpResponseRedirect('/CHproto/profile')


@login_required
def editcourse(request, course_id):
    course = Course.objects.get(pk=course_id)
    if request.method =="POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            return HttpResponseRedirect('/CHproto/profile/')
    else:
        form = CourseForm(instance=course)
    return render(request, 'editcourse.html', {'form': form, 'course': course})

@login_required
def addattendance(request, student_id, course_id):
    roster = Roster.objects.get(student=student_id, course=course_id)
    course = Course.objects.get(pk=course_id)
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=True)
            attendance.roster = roster
            attendance.save()
            return HttpResponseRedirect('/CHproto/%i/roster/' % course.id)
    else:
        form = AttendanceForm()
    return render(request, 'addattendance.html', {'form': form})

@login_required
def newattendance(request, student_id, course_id):
    roster = Roster.objects.get(student=student_id, course=course_id)
    course = Course.objects.get(pk=course_id)
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=True)
            return HttpResponseRedirect('/CHproto/%i/roster/' % course.id)
    else:
        form = AttendanceForm()
    return render(request, 'addattendance.html', {'form': form})

@login_required
def attendance(request, course_id):
    course = Course.objects.get(pk=course_id)
    roster_entries = Roster.objects.filter(course=course)

    #attendances = {} # student: attendance1, attendance2, etc.
    m1_a = {}
    m2_a = {}
    m3_a = {}
    m4_a = {}

    m1_total = {}
    m2_total = {}
    m3_total = {}
    m4_total = {}

    all_totals = {}

    students = []

    for roster_entry in roster_entries:
        curr_student = Student.objects.get(pk=roster_entry.student.pk)
        students.append(curr_student)

        #attendances[curr_student] = Attendance.objects.filter(roster=roster_entry.pk).order_by('date')
        m1_a[curr_student] = Attendance.objects.filter(roster=roster_entry.pk, month_number=1).order_by('date')
        m2_a[curr_student] = Attendance.objects.filter(roster=roster_entry.pk, month_number=2).order_by('date')
        m3_a[curr_student] = Attendance.objects.filter(roster=roster_entry.pk, month_number=3).order_by('date')
        m4_a[curr_student] = Attendance.objects.filter(roster=roster_entry.pk, month_number=4).order_by('date')

        #m1_total[curr_student] = 0
        m1_total = 0
        m2_total = 0
        m3_total = 0
        m4_total = 0

        for value in m1_a[curr_student]:
            m1_total += value.hours_attended

        for value in m2_a[curr_student]:
            m2_total += value.hours_attended

        for value in m3_a[curr_student]:
            m3_total += value.hours_attended

        for value in m4_a[curr_student]:
            m4_total += value.hours_attended

        overall_hours = m1_total+m2_total+m3_total+m4_total

        all_totals[curr_student] = [m1_total, m2_total, m3_total, m4_total, overall_hours]

    context = {
        'course': course,
        'm1_total': m1_total,
        'm2_total': m2_total,
        'm3_total': m3_total,
        'm4_total': m4_total,
        'all_totals': all_totals,
        #'attendances': attendances.items(),
        'roster_entries': roster_entries,
        'students': students,
    }

    template = loader.get_template('att.html')

    return HttpResponse(template.render(context, request))

@login_required
def graphattendancebymonth(request, course_id, month_number):
    course = Course.objects.get(pk=course_id)
    roster_entries = Roster.objects.filter(course=course)

    month_attendances = []

    for roster in roster_entries:
        month_attendances.append(Attendance.objects.filter(roster=roster,
        month_number=month_number))


    f_a_t = []

    for item in month_attendances:
        if item.attendance_mark == 'FULL':
            f_a_t[0] += 1

        elif item.attendance_mark == 'TARDY':
            f_a_t[3] += 1

        elif item.attendance_mark == 'ABSENT' and item.absent_excused == True:
            f_a_t[1] += 1

        elif item.attendance_mark == 'ABSENT' and item.absent_excused == False:
            f_a_t[2] += 1

    context = {
        'f_a_t': f_a_t,
    }

    template = loader.get_template('graph.html')

    return HttpResponse(template.render(context, request))

@login_required
def graphattendancebyweek(request, course_id, month_number, week_number):
    course = Course.objects.get(pk=course_id)
    roster_entries = Roster.objects.filter(course=course)

    week_attendances = []

    for roster in roster_entries:
        week_attendances.append(Attendance.objects.filter(roster=roster,
        month_number=month_number, week_number=week_number))


    f_a_t = []

    for item in week_attendances:
        if item.attendance_mark == 'FULL':
            f_a_t[0] += 1

        elif item.attendance_mark == 'TARDY':
            f_a_t[3] += 1

        elif item.attendance_mark == 'ABSENT' and item.absent_excused == True:
            f_a_t[1] += 1

        elif item.attendance_mark == 'ABSENT' and item.absent_excused == False:
            f_a_t[2] += 1

    context = {
        'f_a_t': f_a_t,
    }

    template = loader.get_template('graph.html')

    return HttpResponse(template.render(context, request))
