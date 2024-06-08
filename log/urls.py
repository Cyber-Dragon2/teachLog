# urls of Polls app

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("signup", views.handleSignup, name="handleSignup"),
    path("take/", views.takeAttendance, name="takeAttendance"),
    path("view/", views.viewAttendance, name="viewAttendance"),
    path("report/", views.viewReport, name="viewReport"),
    path("signin", views.handleSignin, name="handleSignin"),
    path("signout", views.handleSignout, name="handleSignout"),
]