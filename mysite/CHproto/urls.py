from django.conf.urls import url, include

from . import views

urlpatterns = [
    url('^register/', views.register, name='register'),



    url(r'^(?P<student_id>[0-9]+)/(?P<course_id>[0-9]+)/addattendance/$', views.addattendance, name='addattendance'),
    #url(r'^(?P<student_id>[0-9]+)/(?P<course_id>[0-9]+)/newattendance/$', views.newattendance, name='newattendance'),

    #url(r'^(?P<student_id>[0-9]+)/(?P<course_id>[0-9]+)/graph/$', views.graph, name='graph'),

    url(r'^(?P<course_id>[0-9]+)/attendance/$', views.attendance, name='attendance'),
    url(r'^(?P<course_id>[0-9]+)/removecourse/$', views.removecourse, name='removecourse'),
    url(r'^newcourse/$', views.newcourse, name='newcourse'),
    url(r'^(?P<course_id>[0-9]+)/editcourse/$', views.editcourse, name='editcourse'),
    url(r'^(?P<student_id>[0-9]+)/(?P<course_id>[0-9]+)/removefromroster/$', views.removefromroster, name='removefromroster'),
    url(r'^(?P<course_id>[0-9]+)/roster/newstudent/$', views.newstudent, name='newstudent'),
    url(r'^(?P<student_id>[0-9]+)/(?P<course_id>[0-9]+)/editstudent/$', views.editstudent, name='editstudent'),
    url(r'^(?P<course_id>[0-9]+)/roster/$', views.roster, name='roster'),
    url(r'^(?P<student_id>[0-9]+)/(?P<course_id>[0-9]+)/graphattendanceoverall/$', views.graphattendanceoverall, name='graphattendanceoverall'),
    url(r'^(?P<student_id>[0-9]+)/(?P<course_id>[0-9]+)/(?P<month_number>[0-9]+)/graphattendancebymonth/$', views.graphattendancebymonth, name='graphattendancebymonth'),
    url(r'^(?P<course_id>[0-9]+)/(?P<month_number>[0-9]+)/graphoverallmonth/$', views.graphoverallmonth, name='graphoverallmonth'),
    url(r'^(?P<student_id>[0-9]+)/(?P<course_id>[0-9]+)/(?P<week_number>[0-9]+)/graphattendancebyweek/$', views.graphattendancebyweek, name='graphattendancebyweek'),

    url(r'^profile/$', views.profile, name='profile'),
    #url(r'^$', views.index, name='index'),
    url('^', include('django.contrib.auth.urls')),
]
