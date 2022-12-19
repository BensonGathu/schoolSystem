from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib import messages
import json
from .forms import staffApplyLeaveForm,staffUpdateProfileForm,addResultsForm

from .models import User, SessionYearModel, StudentResult, Staffs, FeedBackStaffs, NotificationStaffs, Classes, Subjects, Students, StudentResult, FeedBackStudent, NotificationStudent, Timetable, Exams,LeaveReportStaff


def staff_home(request):
	# Fetching All Students under Staff
    try:
        classteacher_to = Classes.objects.filter(class_teacher=request.user.id)
    except:
        return None
    subjects = Subjects.objects.filter(staff_id=request.user.id)
	# classes_id_list = []
	# for subject in subjects:
	# 	classes = Classes.objects.filter(sessionperiod_id=subject.class_id.sessionperiod)
	# 	print(classes)
	# 	classes_id_list.append(classes)
     
    # final_classes = []
	# # Removing Duplicate Course Id 
    # for class_id in classes_id_list:
    #     if class_id not in final_classes:
    #         final_classes.append(class_id)
			
    # print(final_classes)
    # students_count = Students.objects.filter(student_class__in=final_classes).count()
    # subject_count = subjects.count()
    # print(subject_count)
    # print(students_count)
	
	# Fetch All Attendance Count
	#attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
	
	# Fetch All Approve Leave
	# print(request.user)
    #  
   
    staff = Staffs.objects.all()
 


    leave_count = LeaveReportStaff.objects.filter(staff_id=request.user.id,
                                                  leave_status=1).count()
    
	
	# Fetch Attendance Data by Subjects
	# subject_list = []
	# attendance_list = []
	# for subject in subjects:
	# 	attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
	# 	subject_list.append(subject.subject_name)
	# 	attendance_list.append(attendance_count1)

	# students_attendance = Students.objects.filter(course_id__in=final_course)
	# student_list = []
	# student_list_attendance_present = []
	# student_list_attendance_absent = []
	# for student in students_attendance:
	# 	attendance_present_count = AttendanceReport.objects.filter(status=True,
	# 															student_id=student.id).count()
	# 	attendance_absent_count = AttendanceReport.objects.filter(status=False,
	# 															student_id=student.id).count()
	# 	student_list.append(student.users_type.first_name+" "+ student.users_type.last_name)
	# 	student_list_attendance_present.append(attendance_present_count)
	# 	student_list_attendance_absent.append(attendance_absent_count)
    
    context={
		# "students_count": students_count,
		# "attendance_count": attendance_count,
		"room_name":"broadcast",
		"leave_count": leave_count,
		"classteacher_to":classteacher_to
		# "subject_count": subject_count,
		# "subject_list": final_classes,
		# "attendance_list": attendance_list,
		# "student_list": students_count,
		# "attendance_present_list": student_list_attendance_present,
		# "attendance_absent_list": student_list_attendance_absent
	}
    return render(request, "Staff_templates/teacher-dashboard.html", context)



def staff_take_attendance(request):
	subjects = Subjects.objects.filter(staff_id=request.user.id)
	session_years = SessionYearModel.objects.all()
	context = {
		"subjects": subjects,
		"session_years": session_years
	}
	return render(request, "staff_template/take_attendance_template.html", context)





def staff_apply_leave(request):
	staff_obj = Staffs.objects.get(users_type=request.user.id)
	my_leaves =LeaveReportStaff.objects.filter(staff_id=staff_obj)
    
	if request.method == "POST":
		form = staffApplyLeaveForm(request.POST, request.FILES)
		if form.is_valid():
			leave_type = form.cleaned_data['leave_type']
			start_leave_date = form.cleaned_data['start_leave_date']
			end_leave_date = form.cleaned_data['end_leave_date']
			leave_message = form.cleaned_data['leave_message']

			staff_obj = Staffs.objects.get(users_type=request.user.id)
		try:
			leave_report = LeaveReportStaff.objects.create(staff_id=staff_obj,
											leave_type=leave_type,
											start_leave_date=start_leave_date,
											end_leave_date=end_leave_date,
											leave_message=leave_message,
											leave_status=0)

			print("leave report",leave_report)
			leave_report.save()
			messages.success(request, "Applied for Leave.")
			return redirect('school:staff_apply_leave')
		except:
			messages.error(request, "Failed to Apply Leave")
			return redirect('school:staff_apply_leave')

	form = staffApplyLeaveForm()
	context = {
		"my_leaves":my_leaves,
		"form":form
	}

	return render(request, "Staff_templates/leave.html",context)

def staff_feedback(request):
    return render(request, "staff_template/staff_feedback_template.html")


def staff_feedback_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method.")
		return redirect('staff_feedback')
	else:
		feedback = request.POST.get('feedback_message')
		staff_obj = Staffs.objects.get(users_type=request.user.id)

		try:
			add_feedback = FeedBackStaffs(staff_id=staff_obj,
										feedback=feedback,
										feedback_reply="")
			add_feedback.save()
			messages.success(request, "Feedback Sent.")
			return redirect('staff_feedback')
		except:
			messages.error(request, "Failed to Send Feedback.")
			return redirect('staff_feedback')



@csrf_exempt
def get_students(request):

	subject_id = request.POST.get("subject")
	session_year = request.POST.get("session_year")

	# Students enroll to Course, Course has Subjects
	# Getting all data from subject model based on subject_id
	subject_model = Subjects.objects.get(id=subject_id)

	session_model = SessionYearModel.objects.get(id=session_year)

	students = Students.objects.filter(subject_id=subject_model.class_id,
									session_year_id=session_model)

	# Only Passing Student Id and Student Name Only
	list_data = []

	for student in students:
		data_small={"id":student.users_type.id,
					"name":student.users_type.first_name+" "+student.users_type.last_name}
		list_data.append(data_small)

	return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)




# @csrf_exempt
# def save_attendance_data(request):

# 	# Get Values from Staf Take Attendance form via AJAX (JavaScript)
# 	# Use getlist to access HTML Array/List Input Data
# 	student_ids = request.POST.get("student_ids")
# 	subject_id = request.POST.get("subject_id")
# 	attendance_date = request.POST.get("attendance_date")
# 	session_year_id = request.POST.get("session_year_id")

# 	subject_model = Subjects.objects.get(id=subject_id)
# 	session_year_model = SessionYearModel.objects.get(id=session_year_id)

# 	json_student = json.loads(student_ids)
	
# 	try:
# 		# First Attendance Data is Saved on Attendance Model
# 		attendance = Attendance(subject_id=subject_model,
# 								attendance_date=attendance_date,
# 								session_year_id=session_year_model)
# 		attendance.save()

# 		for stud in json_student:
# 			# Attendance of Individual Student saved on AttendanceReport Model
# 			student = Students.objects.get(users_type=stud['id'])
# 			attendance_report = AttendanceReport(student_id=student,
# 												attendance_id=attendance,
# 												status=stud['status'])
# 			attendance_report.save()
# 		return HttpResponse("OK")
# 	except:
# 		return HttpResponse("Error")




# def staff_update_attendance(request):
# 	subjects = Subjects.objects.filter(staff_id=request.user.id)
# 	session_years = SessionYearModel.objects.all()
# 	context = {
# 		"subjects": subjects,
# 		"session_years": session_years
# 	}
# 	return render(request, "staff_template/update_attendance_template.html", context)

# @csrf_exempt
# def get_attendance_dates(request):
	

# 	# Getting Values from Ajax POST 'Fetch Student'
# 	subject_id = request.POST.get("subject")
# 	session_year = request.POST.get("session_year_id")

# 	# Students enroll to Course, Course has Subjects
# 	# Getting all data from subject model based on subject_id
# 	subject_model = Subjects.objects.get(id=subject_id)

# 	session_model = SessionYearModel.objects.get(id=session_year)
# 	attendance = Attendance.objects.filter(subject_id=subject_model,
# 										session_year_id=session_model)

# 	# Only Passing Student Id and Student Name Only
# 	list_data = []

# 	for attendance_single in attendance:
# 		data_small={"id":attendance_single.id,
# 					"attendance_date":str(attendance_single.attendance_date),
# 					"session_year_id":attendance_single.session_year_id.id}
# 		list_data.append(data_small)

# 	return JsonResponse(json.dumps(list_data),
# 						content_type="application/json", safe=False)


# @csrf_exempt
# def get_attendance_student(request):

# 	# Getting Values from Ajax POST 'Fetch Student'
# 	attendance_date = request.POST.get('attendance_date')
# 	attendance = Attendance.objects.get(id=attendance_date)

# 	attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
# 	# Only Passing Student Id and Student Name Only
# 	list_data = []

# 	for student in attendance_data:
# 		data_small={"id":student.student_id.users_type.id,
# 					"name":student.student_id.users_type.first_name+" "+student.student_id.users_type.last_name, "status":student.status}
# 		list_data.append(data_small)

# 	return JsonResponse(json.dumps(list_data),
# 						content_type="application/json",
# 						safe=False)


# @csrf_exempt
# def update_attendance_data(request):
# 	student_ids = request.POST.get("student_ids")

# 	attendance_date = request.POST.get("attendance_date")
# 	attendance = Attendance.objects.get(id=attendance_date)

# 	json_student = json.loads(student_ids)

# 	try:
		
# 		for stud in json_student:
		
# 			# Attendance of Individual Student saved on AttendanceReport Model
# 			student = Students.objects.get(users_type=stud['id'])

# 			attendance_report = AttendanceReport.objects.get(student_id=student,
# 															attendance_id=attendance)
# 			attendance_report.status=stud['status']

# 			attendance_report.save()
# 		return HttpResponse("OK")
# 	except:
# 		return HttpResponse("Error")


def staff_profile(request):
	user = CustomUser.objects.get(id=request.user.id)
	staff = Staffs.objects.get(users_type=user)
	form = staffUpdateProfileForm()
	form.fields["username"].initial = user.users_type.username
	form.fields["first_name"].initial = user.users_type.first_name
	form.fields["last_name"].initial = user.users_type.last_name
	form.fields["password"].initial = user.users_type.password
	form.fields["email"].initial = user.users_type.email
	form.fields["profile_pic"].initial = user.users_type.profile_pic
	context={
		"user": user,
		"staff": staff,
		"form":form
	}
	return render(request, 'staff_template/staff_profile.html', context)
 

def staff_profile_update(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method!")
		return redirect('staff_profile')
	else:
		form = staffUpdateProfileForm(request.POST, request.FILES)
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

			staff = Staffs.objects.get(users_type=customuser.id)
			staff.address = address
			staff.profile_pic = profile_pic
			staff.save()

			messages.success(request, "Profile Updated Successfully")
			return redirect('staff_profile')
		except:
			messages.error(request, "Failed to Update Profile")
			return redirect('staff_profile')



def staff_add_result(request):
	subjects = Subjects.objects.filter(staff_id=request.user.id)
	class_list = []
	for subject in subjects:
		class_list.append(subject.class_id.name)
	final_class_list= set(class_list)
	session_years = SessionYearModel.objects.all()
	context = {
		"subjects": subjects,
		"session_years": session_years,
		"final_class_list":final_class_list
	}
	return render(request, "Staff_templates/add_result.html", context)

def staff_students(request,subject_id):
	current_subject = get_object_or_404(Subjects,id=subject_id)
	students = []

	all_students =  Students.objects.all()
	for student in all_students:
		for subject in student.subject_id.all():
			if subject.id == int(subject_id):
				students.append(student)
	
	context = {
		"students": students,
		"current_subject":current_subject
	} 
	return render(request, 'Staff_templates/students.html', context)

def staff_students_all(request):
	students = []

	all_students =  Students.objects.all()
	for student in all_students:
		for subject in student.subject_id.all():
			if subject.staff_id == request.user:
				students.append(student)
	
	context = {
		"students": students,
	} 
	return render(request, 'Staff_templates/all_students.html', context)


def staff_add_marks(request,studentID,subjectID):
	student_obj = get_object_or_404(Students,id=studentID)
	subject_obj =get_object_or_404(Subjects,id=subjectID)
	form = addResultsForm()
	if request.method == "POST":
		form = addResultsForm(request.POST)
		if form.is_valid():
			marks = form.save(commit=False)
			marks.student = student_obj
			marks.subjects = subject_obj
			
			marks.teacher = request.user.username
			marks.save()

		try:
			# Check if Students Result Already Exists or not
			check_exist = StudentResult.objects.filter(subject_id=subject_obj,
													student_id=student_obj).exists()
			if check_exist:
				result = StudentResult.objects.get(subject_id=subject_obj,
												student_id=student_obj)
				result.subject_assignment_marks = assignment_marks
				result.subject_exam_marks = exam_marks
				result.save()
				messages.success(request, "Result Updated Successfully!")
				return redirect('staff_add_result')
			else:
				result = StudentResult(student_id=student_obj,
									subject_id=subject_obj,
									subject_exam_marks=exam_marks,
									subject_assignment_marks=assignment_marks)
				result.save()
				messages.success(request, "Result Added Successfully!")
				return redirect('staff_add_result')
		except:
			messages.error(request, "Failed to Add Result!")
			return redirect('staff_add_result')

