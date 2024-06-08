# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.user.username

class Student(models.Model):
    uid = models.IntegerField(default=0, null=False, blank=False, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date}"

class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_classes_attended = models.IntegerField(default=0)
    total_classes_held = models.IntegerField(default=0)

    @property
    def attendance_percentage(self):
        if self.total_classes_held == 0:
            return 0
        return (self.total_classes_attended / self.total_classes_held) * 100

    def __str__(self):
        return f"{self.student} - {self.subject}"
