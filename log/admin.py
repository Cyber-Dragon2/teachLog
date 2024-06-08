from django.contrib import admin
from .models import Subject, Teacher, Student, Attendance, AttendanceReport

admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
