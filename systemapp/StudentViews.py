from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import datetime
from django.contrib import messages
from .forms import studentUpdateProfileForm 
from .models import CustomUser, SessionYearModel, StudentResult, Admin, Staffs, FeedBackStaffs, NotificationStaffs, Classes, Subjects, Students, StudentResult, FeedBackStudent, NotificationStudent, Timetable, Exams
def student_home(request):
    student_obj = Students.objects.get(users_type=request.user.id)
    # total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
    # attendance_present = AttendanceReport.objects.filter(student_id=student_obj,
    #                                                     status=True).count()
    # attendance_absent = AttendanceReport.objects.filter(student_id=student_obj,
    #                                                     status=False).count()
    class_obj = Classes.objects.get(id=student_obj.student_class.id)
    # total_subjects = Subjects.objects.filter(course_id=class_obj).count()
    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(session_id=student_obj.session_year_id)
    for subject in subject_data:
        # attendance = Attendance.objects.filter(subject_id=subject.id)
        # attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance,
        #                                                         status=True,
        #                                                         student_id=student_obj.id).count()
        # attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance,
        #                                                         status=False,
        #                                                         student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        # data_present.append(attendance_present_count)
        # data_absent.append(attendance_absent_count)
        
        context={
            # "total_attendance": total_attendance,
            # "attendance_present": attendance_present,
            # "attendance_absent": attendance_absent,
            # "total_subjects": total_subjects,
            "subject_name": subject_name,
            "data_present": data_present,
            "data_absent": data_absent
        }
        return render(request, "student-dashboard.html")


def student_view_attendance(request):

	# Getting Logged in Student Data
	student = Students.objects.get(users_type=request.user.id)
	
	# Getting Course Enrolled of LoggedIn Student
	course = student.course_id
	
	# Getting the Subjects of Course Enrolled
	subjects = Subjects.objects.filter(course_id=course)
	context = {
		"subjects": subjects
	}
	return render(request, "student_template/student_view_attendance.html", context)


# def student_view_attendance_post(request):
# 	if request.method != "POST":
# 		messages.error(request, "Invalid Method")
# 		return redirect('student_view_attendance')
# 	else:
# 		# Getting all the Input Data
# 		subject_id = request.POST.get('subject')
# 		start_date = request.POST.get('start_date')
# 		end_date = request.POST.get('end_date')

# 		# Parsing the date data into Python object
# 		start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
# 		end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

# 		# Getting all the Subject Data based on Selected Subject
# 		subject_obj = Subjects.objects.get(id=subject_id)
		
# 		# Getting Logged In User Data
# 		user_obj = CustomUser.objects.get(id=request.user.id)
		
# 		# Getting Student Data Based on Logged in Data
# 		stud_obj = Students.objects.get(users_type=user_obj)

# 		# Now Accessing Attendance Data based on the Range of Date
# 		# Selected and Subject Selected
# 		attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse,
# 																	end_date_parse),
# 											subject_id=subject_obj)
# 		# Getting Attendance Report based on the attendance
# 		# details obtained above
# 		attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance,
# 															student_id=stud_obj)

		
# 		context = {
# 			"subject_obj": subject_obj,
# 			"attendance_reports": attendance_reports
# 		}

# 		return render(request, 'student_template/student_attendance_data.html', context)
		

# def student_apply_leave(request):
# 	student_obj = Students.objects.get(users_type=request.user.id)
# 	leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
# 	context = {
# 		"leave_data": leave_data
# 	}
# 	return render(request, 'student_template/student_apply_leave.html', context)


# def student_apply_leave_save(request):
# 	if request.method != "POST":
# 		messages.error(request, "Invalid Method")
# 		return redirect('student_apply_leave')
# 	else:
# 		leave_date = request.POST.get('leave_date')
# 		leave_message = request.POST.get('leave_message')

# 		student_obj = Students.objects.get(users_type=request.user.id)
# 		try:
# 			leave_report = LeaveReportStudent(student_id=student_obj,
# 											leave_date=leave_date,
# 											leave_message=leave_message,
# 											leave_status=0)
# 			leave_report.save()
# 			messages.success(request, "Applied for Leave.")
# 			return redirect('student_apply_leave')
# 		except:
# 			messages.error(request, "Failed to Apply Leave")
# 			return redirect('student_apply_leave')


def student_feedback(request):
	student_obj = Students.objects.get(users_type=request.user.id)
	feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
	context = {
		"feedback_data": feedback_data
	}
	return render(request, 'student_template/student_feedback.html', context)


def student_feedback_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method.")
		return redirect('student_feedback')
	else:
		feedback = request.POST.get('feedback_message')
		student_obj = Students.objects.get(users_type=request.user.id)

		try:
			add_feedback = FeedBackStudent(student_id=student_obj,
										feedback=feedback,
										feedback_reply="")
			add_feedback.save()
			messages.success(request, "Feedback Sent.")
			return redirect('student_feedback')
		except:
			messages.error(request, "Failed to Send Feedback.")
			return redirect('student_feedback')


def student_profile(request):
	user = CustomUser.objects.get(id=request.user.id)
	student = Students.objects.get(users_type=user)
	
	form = studentUpdateProfileForm()
	form.fields["username"].initial = user.users_type.username
	form.fields["first_name"].initial = user.users_type.first_name
	form.fields["last_name"].initial = user.users_type.last_name
	form.fields["password"].initial = user.users_type.password
	form.fields["email"].initial = user.users_type.email
	form.fields["profile_pic"].initial = user.users_type.profile_pic

	context={
		"user": user,
		"student": student,
		"form":form
	}
	return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method!")
		return redirect('student_profile')
	else:
		form = studentUpdateProfileForm(request.POST, request.FILES)
		if form.is_valid():

			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			address = form.cleaned_data['address']
			profile_pic = form.cleaned_data['profile_pic']
		try:
			customuser = CustomUser.objects.get(id=request.user.id)
			customuser.username = username
			customuser.first_name = first_name
			customuser.last_name = last_name
			customuser.email = email
		
			if password != None and password != "":
				customuser.set_password(password)
			customuser.save() 

			student = Students.objects.get(users_type=customuser.id)
			student.address = address
			student.profile_pic = profile_pic
			student.save()
			
			messages.success(request, "Profile Updated Successfully")
			return redirect('student_profile')
		except:
			messages.error(request, "Failed to Update Profile")
			return redirect('student_profile')


def student_view_result(request):
	student = Students.objects.get(users_type=request.user.id)
	student_result = StudentResult.objects.filter(student_id=student.id)
	context = {
		"student_result": student_result,
	}
	return render(request, "student_template/student_view_result.html", context)
