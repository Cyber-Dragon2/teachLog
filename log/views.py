
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Subject, Teacher, Student, Attendance, AttendanceReport
from datetime import date, datetime
# Create your views here.

def home(request):
    students = Student.objects.all()
    if request.method == 'POST':
        # Process form submission
        teacher = Teacher.objects.get(user=request.user)
        subject = teacher.subject      
        
        for student in students:
            attendance_status = request.POST.get(f'attendance_{student.id}')
            statusVal = True if attendance_status == 'present' else False
            # Create Attendance object and save it
            attendance = Attendance.objects.create(
                student=student,
                date=date.today(),
                subject = subject,
                is_present=statusVal
            )
            # save attendance of marked student
            attendance.save()
            
            report, created = AttendanceReport.objects.get_or_create(
                student=student,
                subject=subject,
                defaults={'total_classes_attended': 0, 'total_classes_held': 0}
        	)
        
        	# Update total classes attended and held based on attendance data
            if attendance_status == 'present':
                report.total_classes_attended += 1
            report.total_classes_held += 1
			# Save the updated AttendanceReport object
            report.save()
           
        messages.success(request, "Recorded Attendance Successfully!")
        return redirect('/')
        
    subs = Subject.objects.values_list('name', flat=True)
    try:
    	teacherSubject = Teacher.objects.get(user = request.user).subject
    except:
        teacherSubject = 'NULL'
    context = {'subjects': subs, 'teacherSubject': teacherSubject}
    return render(request, "home.html", context)

def about(request):
    return render(request, 'about.html')

def viewReport(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()
    attendance_report = None
    result = None
    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        print(f"Selected Subject : {subject_id}")
        print(f"Selected Student : {student_id}")
        subject = Subject.objects.get(id = subject_id)
        student = Student.objects.get(id=student_id)
        attendance_report = AttendanceReport.objects.filter(student=student, subject=subject).first()
        
        if not attendance_report:
            messages.error(request, "Didn't found Report for entered data")
            result = "404 - Report Not Found"
            
    context = {'students' : students, 'subjects' : subjects, 'attendance_report': attendance_report,'result' : result}
    return render(request, 'viewReport.html', context)

def viewAttendance(request):
    subs = Subject.objects.values_list('name', flat=True)
    attendance_data = None
    if request.method == 'POST':
        selected_date = request.POST.get('date')
        selected_subject = request.POST.get('subject')
        print(f"date: {selected_date}\nsubject: {selected_subject}")
        
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        subjectModel = Subject.objects.get(name=selected_subject)
        attendance_data = Attendance.objects.filter(date=selected_date, subject=subjectModel)
        if not attendance_data:
            messages.error(request, "No Attendance was recoreded for entered Date")

    context = {'subjects': subs, 'attendance_data': attendance_data}
    return render(request, 'viewAttendance.html', context)

def takeAttendance(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        subject = teacher.subject
        todaysDate = datetime.now().strftime('%Y-%m-%d')
		# Check if attendance has already been taken for the selected date and subject
        if Attendance.objects.filter(date=todaysDate, subject=subject).exists():
            messages.error(request, 'Attendance for this date and subject has already been recorded.')
            return redirect('/')  # Redirect to the same page or a different page
        students = Student.objects.all()
        context = {'students': students}
        return render(request, 'takeAttendance.html', context)
    except Exception as e:
        return HttpResponse('404 - Not Found')

def handleSignup(request):
    if request.method =='POST':
        # Get parameters
        username = request.POST['Username']
        password = request.POST['Password1']
        password2 = request.POST['Password2']
        subject = request.POST['Subject']
        subjectModel = Subject.objects.get(name=subject)
        if password == password2:
            myUser = User.objects.create_user(username,password=password)
            # Create Teacher
            try:
                teacher = Teacher(user=myUser, subject=subjectModel)
                teacher.save()
            except Exception as e:
                print(e)
            else:
                myUser.save()
                print("yes")
                messages.success(request, "Your Account was created Successfully")
        else:
            print("no")
            messages.error(request, "Your entered password didn't match!! Try Again.")

        print(username)
        print(password)
        print(password2)
        # return render(request, "home.html")
        return redirect("/")

    else:
        return HttpResponse('404 - Not Found')
    


def handleSignin(request):
    if request.method =='POST':
        # Get parameters
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Succesfully")
        else:
            messages.error(request, "Invalid credentials, Please Try Again!")  
        
        return redirect('/')

    else:
        return HttpResponse('404 - Not Found')
    

def handleSignout(request):
    logout(request)
    messages.success(request, "Logged out Succesfully")
    return redirect('/')
  