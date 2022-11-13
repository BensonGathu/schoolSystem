from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import AddStudentForm, EditStudentForm,addClassForm,editClassForm,addSessionYearModelForm,editSessionYearModelForm,addSubjectForm,editSubjectForm,addLeaveReportStaff,addFeedBackStaffs,addNotificationStaffs,addStaffForm,editStaffForm,adminUpdateProfileForm

from .models import CustomUser, SessionYearModel, StudentResult, Staffs, FeedBackStaffs, NotificationStaffs, Classes, Subjects, Students, StudentResult, FeedBackStudent, NotificationStudent, Timetable, Exams,LeaveReportStaff,Admin

	#managing session periods
def manage_session(request):
	session_years = SessionYearModel.objects.all()
	context = {
		"session_years": session_years
	}
	return render(request, "admin_templates/manage_session_template.html", context)


def add_session(request):
	form = addSessionYearModelForm()
	context = {
		"form":form
	}
	return render(request, "admin_templates/add_session_template.html",context)


def add_session_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('add_course')
	else:
		form = addSessionYearModelForm(request.POST, request.FILES)
		if form.is_valid():

			session_start_year = form.cleaned_data['session_start_year']
			session_end_year = form.cleaned_data['session_end_year']

		try:
			sessionyear = SessionYearModel(session_start_year=session_start_year,
										session_end_year=session_end_year)
			sessionyear.save()
			messages.success(request, "Session Year added Successfully!")
			return redirect("add_session")
		except:
			messages.error(request, "Failed to Add Session Year")
			return redirect("add_session")


def edit_session(request, session_id):
	session_year = SessionYearModel.objects.get(id=session_id)
	# Adding Student ID into Session Variable
	request.session['session_id'] = session_id

	form = editSessionYearModelForm() 
	form.fields["session_start_year"].initial = session_year.session_start_year
	form.fields["session_end_year"].initial = session_year.session_end_year

	context = {
		"session_year": session_year,
		"form":form
	}
	return render(request, "admin_templates/edit_session_template.html", context)


def edit_session_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method!")
		return redirect('manage_session')
	else:
		session_id = request.session.get('session_id')
		if session_id == None:
			return redirect("/manage_session")

		form = editSessionYearModelForm(request.POST, request.FILES)
		if form.is_valid():

			session_start_year = form.cleaned_data['session_start_year']
			session_end_year = form.cleaned_data['session_end_year']

		try:
			session_year = SessionYearModel.objects.get(id=session_id)
			session_year.session_start_year = session_start_year
			session_year.session_end_year = session_end_year
			session_year.save()
			# Delete  SESSION after the data is updated
			del request.session['session_id']

			messages.success(request, "Session Year Updated Successfully.")
			return redirect('/edit_session/'+session_id)
		except:
			messages.error(request, "Failed to Update Session Year.")
			return redirect('/edit_session/'+session_id)


def delete_session(request, session_id):
	session = SessionYearModel.objects.get(id=session_id)
	try:
		session.delete()
		messages.success(request, "Session Deleted Successfully.")
		return redirect('manage_session')
	except:
		messages.error(request, "Failed to Delete Session.")
		return redirect('manage_session')


def admin_home(request):
	
	all_student_count = Students.objects.all().count()
	subject_count = Subjects.objects.all().count()
	classess_count = Classes.objects.all().count()
	staff_count = Staffs.objects.all().count()
	classess_all = Classes.objects.all()
	classess_name_list = []
	subject_count_list = []
	student_count_list_in_class = []

	for classess in classess_all:
		subjects = Subjects.objects.filter(class_id=classess.id).count()
		students = Students.objects.filter(student_class=classess.id).count()
		classess_name_list.append(classess.name)
		subject_count_list.append(subjects)
		student_count_list_in_class.append(students)
	
	subject_all = Subjects.objects.all()
	subject_list = []
	student_count_list_in_subject = []
	for subject in subject_all:
		classess = Classes.objects.get(id=subject.class_id.id)
		student_count = Students.objects.filter(student_class=subject.id).count()
		subject_list.append(subject.subject_name)
		student_count_list_in_subject.append(student_count)
	
	# For Saffs
	staff_attendance_present_list=[]
	staff_attendance_leave_list=[]
	staff_name_list=[]

	staffs = Staffs.objects.all()
	for staff in staffs:
		subject_ids = Subjects.objects.filter(staff_id=staff.users_type.id)
		#attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
		leaves = LeaveReportStaff.objects.filter(staff_id=staff.id,
												leave_status=1).count()
		#staff_attendance_present_list.append(attendance)
		staff_attendance_leave_list.append(leaves)
		staff_name_list.append(staff.users_type.first_name)

	# For Students
	#student_attendance_present_list=[]
	#student_attendance_leave_list=[]
	student_name_list=[]

	students = Students.objects.all()
	for student in students:
		# attendance = AttendanceReport.objects.filter(student_id=student.id,
		# 											status=True).count()
		# absent = AttendanceReport.objects.filter(student_id=student.id,
		# 										status=False).count()
		# leaves = LeaveReportStudent.objects.filter(student_id=student.id,
		# 										leave_status=1).count()
		# student_attendance_present_list.append(attendance)
		# student_attendance_leave_list.append(leaves+absent)
		student_name_list.append(student.users_type.first_name)


	context={
		"all_student_count": all_student_count,
		"subject_count": subject_count,
		"class_count": classess_count,
		"staff_count": staff_count,
		"classess_name_list": classess_name_list,
		"subject_count_list": subject_count_list,
		"student_count_list_in_class": student_count_list_in_class,
		"subject_list": subject_list,
		"student_count_list_in_subject": student_count_list_in_subject,
		"staff_attendance_present_list": staff_attendance_present_list,
		"staff_attendance_leave_list": staff_attendance_leave_list,
		"staff_name_list": staff_name_list,
		# "student_attendance_present_list": student_attendance_present_list,
		# "student_attendance_leave_list": student_attendance_leave_list,
		"student_name_list": student_name_list,
	}
	return render(request, "admin_templates/home_content.html", context)


def add_staff(request):
	form = addStaffForm()
	context = {
		"form": form
	}
	return render(request, "admin_templates/add_staff_template.html", context)


def add_staff_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method ")
		return redirect('add_staff')
	else:
		form = addStaffForm(request.POST, request.FILES)
		if form.is_valid():

			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			address = form.cleaned_data['address']
			staff_ID = form.cleaned_data['staff_ID']
			national_ID = form.cleaned_data['national_ID']
			gender = form.cleaned_data['gender']

			if len(request.FILES) != 0:
				profile_pic = request.FILES['profile_pic']
				fs = FileSystemStorage()
				filename = fs.save(profile_pic.name, profile_pic)
				profile_pic_url = fs.url(filename)
			else:
				profile_pic_url = None


			try:
				user = CustomUser.objects.create_user(username=username,
													password=password,
													email=email,
													first_name=first_name,
													last_name=last_name,
													user_type=3)
				user.staffs.address = address
				user.staffs.staff_ID = staff_ID
				user.staffs.national_ID = national_ID
				user.staffs.gender = gender
				if profile_pic_url != None:
					user.staffs.profile_pic = profile_pic_url
				user.save()
				messages.success(request, "Staff Added Successfully!")
				return redirect('add_staff')
			except:
				messages.error(request, "Failed to Add Staff!")
				return redirect('add_staff')



def manage_staff(request):
	staffs = Staffs.objects.all()
	context = {
		"staffs": staffs
	}
	return render(request, "admin_templates/manage_staff_template.html", context)


def edit_staff(request, staff_id):
	request.session['staff_id'] = staff_id

	staff = Staffs.objects.get(users_type=staff_id)
	form = editStaffForm()

		# Filling the form with Data from Database
	form.fields['email'].initial = staff.users_type.email
	form.fields['username'].initial = staff.users_type.username
	form.fields['first_name'].initial = staff.users_type.first_name
	form.fields['last_name'].initial = staff.users_type.last_name
	form.fields['address'].initial = staff.address
	form.fields['gender'].initial = staff.gender
	form.fields['national_ID'].initial = staff.national_ID
	form.fields['staff_ID'].initial = staff.staff_ID


	context = {
		"staff": staff,
		"id": staff_id,
		"form":form
	}
	return render(request, "admin_templates/edit_staff_template.html", context)


def edit_staff_save(request):
	if request.method != "POST":
		return HttpResponse("<h2>Method Not Allowed</h2>")
	else:
		staff_id = request.session.get('staff_id')
		if staff_id == None:
			return redirect('/manage_staff')	

		form = editStaffForm(request.POST, request.FILES)
		if form.is_valid():

			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			address = form.cleaned_data['address']
			staff_ID = form.cleaned_data['staff_ID']
			national_ID = form.cleaned_data['national_ID']
			gender = form.cleaned_data['gender']


			if len(request.FILES) != 0:
				profile_pic = request.FILES['profile_pic']
				fs = FileSystemStorage()
				filename = fs.save(profile_pic.name, profile_pic)
				profile_pic_url = fs.url(filename)
			else:
				profile_pic_url = None

			try:
				# INSERTING into Customuser Model
				user = CustomUser.objects.get(id=staff_id)
				user.first_name = first_name
				user.last_name = last_name
				user.email = email
				user.username = username
				user.save()
					
				# INSERTING into Staff Model
				staff_model = Staffs.objects.get(users_type=staff_id)
				staff_model.address = address
				staff_model.national_ID = national_ID
				staff_model.staff_ID = staff_ID
				staff_model.gender = gender
				if profile_pic_url != None:
					staff_model.profile_pic = profile_pic_url
				staff_model.save()
				# Delete  SESSION after the data is updated
				del request.session['staff_id']

				staff_model.save()

				messages.success(request, "Staff Updated Successfully.")
				return redirect('/edit_staff/'+staff_id)

			except:
				messages.error(request, "Failed to Update Staff.")
			return redirect('/edit_staff/'+staff_id)



def delete_staff(request, staff_id):
	staff = Staffs.objects.get(users_type=staff_id)
	try:
		staff.delete()
		messages.success(request, "Staff Deleted Successfully.")
		return redirect('manage_staff')
	except:
		messages.error(request, "Failed to Delete Staff.")
		return redirect('manage_staff')


def add_teacher(request):
	form = addStaffForm()
	context = {
		"form": form
	}
	return render(request, "admin_templates/add_staff_template.html", context)


def add_teacher_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method ")
		return redirect('add_staff')
	else:
		form = addStaffForm(request.POST, request.FILES)
		if form.is_valid():

			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			address = form.cleaned_data['address']
			staff_ID = form.cleaned_data['staff_ID']
			national_ID = form.cleaned_data['national_ID']
			gender = form.cleaned_data['gender']

			if len(request.FILES) != 0:
				profile_pic = request.FILES['profile_pic']
				fs = FileSystemStorage()
				filename = fs.save(profile_pic.name, profile_pic)
				profile_pic_url = fs.url(filename)
			else:
				profile_pic_url = None


			try:
				user = CustomUser.objects.create_user(username=username,
													password=password,
													email=email,
													first_name=first_name,
													last_name=last_name,
													user_type=2)
				user.staffs.address = address
				user.staffs.staff_ID = staff_ID
				user.staffs.national_ID = national_ID
				user.staffs.gender = gender
				user.staffs.profile_pic = profile_pic_url

				user.save()
				messages.success(request, "Staff Added Successfully!")
				return redirect('add_staff')
			except:
				messages.error(request, "Failed to Add Staff!")
				return redirect('add_staff')



def manage_teacher(request):
	staffs = Staffs.objects.all()
	context = {
		"staffs": staffs
	}
	return render(request, "admin_templates/manage_staff_template.html", context)


def edit_teacher(request, staff_id):
	request.session['staff_id'] = staff_id

	staff = Staffs.objects.get(users_type=staff_id)
	form = editStaffForm()

		# Filling the form with Data from Database
	form.fields['email'].initial = staff.users_type.email
	form.fields['username'].initial = staff.users_type.username
	form.fields['first_name'].initial = staff.users_type.first_name
	form.fields['last_name'].initial = staff.users_type.last_name
	form.fields['address'].initial = staff.address
	form.fields['gender'].initial = staff.gender
	form.fields['national_ID'].initial = staff.national_ID
	form.fields['staff_ID'].initial = staff.staff_ID


	context = {
		"staff": staff,
		"id": staff_id,
		"form":form
	}
	return render(request, "admin_templates/edit_staff_template.html", context)


def edit_teacher_save(request):
	if request.method != "POST":
		return HttpResponse("<h2>Method Not Allowed</h2>")
	else:
		staff_id = request.session.get('staff_id')
		if staff_id == None:
			return redirect('/manage_staff')	

		form = editStaffForm(request.POST, request.FILES)
		if form.is_valid():

			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			address = form.cleaned_data['address']
			staff_ID = form.cleaned_data['staff_ID']
			national_ID = form.cleaned_data['national_ID']
			gender = form.cleaned_data['gender']


			if len(request.FILES) != 0:
				profile_pic = request.FILES['profile_pic']
				fs = FileSystemStorage()
				filename = fs.save(profile_pic.name, profile_pic)
				profile_pic_url = fs.url(filename)
			else:
				profile_pic_url = None

			try:
				# INSERTING into Customuser Model
				user = CustomUser.objects.get(id=staff_id)
				user.first_name = first_name
				user.last_name = last_name
				user.email = email
				user.username = username
				user.save()
					
				# INSERTING into Staff Model
				staff_model = Staffs.objects.get(users_type=staff_id)
				staff_model.address = address
				staff_model.national_ID = national_ID
				staff_model.staff_ID = staff_ID
				staff_model.gender = gender
				if profile_pic_url != None:
					staff_model.profile_pic = profile_pic_url
				staff_model.save()
				# Delete  SESSION after the data is updated
				del request.session['staff_id']

				staff_model.save()

				messages.success(request, "Staff Updated Successfully.")
				return redirect('/edit_staff/'+staff_id)

			except:
				messages.error(request, "Failed to Update Staff.")
			return redirect('/edit_staff/'+staff_id)



def delete_staff(request, staff_id):
	staff = Staffs.objects.get(users_type=staff_id)
	try:
		staff.delete()
		messages.success(request, "Staff Deleted Successfully.")
		return redirect('manage_staff')
	except:
		messages.error(request, "Failed to Delete Staff.")
		return redirect('manage_staff')


def add_class(request):
	form = addClassForm()

	context = {"form":form}
	return render(request, "admin_templates/add_class_template.html",context)


def add_class_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method!")
		return redirect('add_class')
	else:
		form = addClassForm(request.POST, request.FILES)
		
		if form.is_valid():
			name =  form.cleaned_data["name"]
			sessionperiod = form.cleaned_data["sessionperiod"]
			class_teacher = form.cleaned_data["class_teacher"]
			new_class = Classes(
				name=name,
				session=sessionperiod,
				class_teacher=class_teacher
			)
			new_class.save()
			
			messages.success(request, "Class Added Successfully!")
			return redirect('add_class')
		
		messages.error(request, "Failed to Add Class!")
		return redirect('add_class')


def manage_class(request):
	classes = Classes.objects.all()
	context = {
		"classes": classes
	}
	return render(request, 'admin_templates/manage_class_template.html', context)


def edit_class(request, class_id):
	classes = Classes.objects.get(id=class_id)

	#adding class ID  into session variable
	request.session["class_id"] = class_id

	form = editClassForm()
	
	# Filling the form with Data from Database
	form.fields["name"]=classes.name
	form.fields["sessionperiod"]=classes.sessionperiod
	form.fields["class_teacher"]=classes.class_teacher
	context = {
		"classes": classes,
		"id": class_id,
		"form":form
	}

	return render(request, 'admin_templates/edit_class_template.html', context)


def edit_class_save(request):
	if request.method != "POST":
		HttpResponse("Invalid Method")
	else:
		class_id = request.session.get('class_id')
		if class_id == None:
			return redirect('/edit_class')

		form = editClassForm()
		if form.is_valid():
			name = form.cleaned_data["name"]
			sessionperiod = form.cleaned_data["sessionperiod"]
			class_teacher = form.cleaned_data["class_teacher"]


			try:
				classes= Classes.objects.get(id=class_id)
				classes.name= name
				classes.sessionperiod=sessionperiod
				classes.class_teacher=class_teacher
				classes.save()
				
				# Delete  SESSION after the data is updated
				del request.session['class_id']
				messages.success(request, "Class Updated Successfully.")
				return redirect('/edit_class/'+class_id)
			except:
				messages.error(request, "Failed to Update class.")
			return redirect('/edit_class/'+class_id)

		else:
			return redirect('/edit_class/'+class_id)


def delete_class(request, class_id):
	classes = Classes.objects.get(id=class_id)
	try:
		classes.delete()
		messages.success(request, "Class Deleted Successfully.")
		return redirect('manage_class')
	except:
		messages.error(request, "Failed to Delete class.")
		return redirect('manage_class')





def add_student(request):
	form = AddStudentForm()
	context = {
		"form": form
	}
	return render(request, 'admin_templates/add_student_template.html', context)




def add_student_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method")
		return redirect('add_student')
	else:
		form = AddStudentForm(request.POST, request.FILES)

		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			address = form.cleaned_data['address']
			session_year_id = form.cleaned_data['session_year_id']
			class_id = form.cleaned_data['class_id']
			subject_id = form.cleaned_data['subject_id']
			kcpe_marks = form.cleaned_data['kcpe_marks']
			gender = form.cleaned_data['gender']

			
			if len(request.FILES) != 0:
				profile_pic = request.FILES['profile_pic']
				fs = FileSystemStorage()
				filename = fs.save(profile_pic.name, profile_pic)
				profile_pic_url = fs.url(filename)
			else:
				profile_pic_url = None


			try:
				user = CustomUser.objects.create_user(username=username,
													password=password,
													email=email,
													first_name=first_name,
													last_name=last_name,
													

													user_type=4)
				user.students.address = address
				user.students.kcpe_marks =kcpe_marks
				subject_obj = Subjects.objects.get(id=subject_id)
				user.students.subject_id =subject_obj

				class_obj = Classes.objects.get(id=class_id)
				user.students.student_class = class_obj



				session_year_obj = SessionYearModel.objects.get(id=session_year_id)
				user.students.session_year_id = session_year_obj

				user.students.gender = gender
				user.students.profile_pic = profile_pic_url
				user.save()
				messages.success(request, "Student Added Successfully!")
				return redirect('add_student')
			except:
				messages.error(request, "Failed to Add Student!")
				return redirect('add_student')
		else:
			return redirect('add_student')


def manage_student(request):
	students = Students.objects.all()
	context = {
		"students": students
	}
	return render(request, 'admin_templates/manage_student_template.html', context)


def edit_student(request, student_id):

	# Adding Student ID into Session Variable
	request.session['student_id'] = student_id

	student = Students.objects.get(users_type=student_id)
	form = EditStudentForm()
	
	# Filling the form with Data from Database
	form.fields['email'].initial = student.users_type.email
	form.fields['username'].initial = student.users_type.username
	form.fields['first_name'].initial = student.users_type.first_name
	form.fields['last_name'].initial = student.users_type.last_name
	form.fields['address'].initial = student.address
	form.fields['student_class'].initial = student.student_class.id
	form.fields['subject_id'].initial = student.subject_id.id
	form.fields['kcpe_marks'].initial = student.kcpe_marks
	form.fields['gender'].initial = student.gender
	form.fields['session_year_id'].initial = student.session_year_id.id

	context = {
		"id": student_id,
		"username": student.users_type.username,
		"form": form
	}
	return render(request, "admin_templates/edit_student_template.html", context)


def edit_student_save(request):
	if request.method != "POST":
		return HttpResponse("Invalid Method!")
	else:
		student_id = request.session.get('student_id')
		if student_id == None:
			return redirect('/manage_student')

		form = EditStudentForm(request.POST, request.FILES)
		if form.is_valid():
			email = form.cleaned_data['email']
			username = form.cleaned_data['username']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			address = form.cleaned_data['address']
			student_class = form.cleaned_data['student_class']
			gender = form.cleaned_data['gender']
			session_year_id = form.cleaned_data['session_year_id']
			subject_id = form.cleaned_data["subject_id"]
			kcpe_marks = form.cleaned_data["kcpe_marks"]


			# Getting Profile Pic first
			# First Check whether the file is selected or not
			# Upload only if file is selected
			if len(request.FILES) != 0:
				profile_pic = request.FILES['profile_pic']
				fs = FileSystemStorage()
				filename = fs.save(profile_pic.name, profile_pic)
				profile_pic_url = fs.url(filename)
			else:
				profile_pic_url = None

			try:
				# First Update into Custom User Model
				user = CustomUser.objects.get(id=student_id)
				user.first_name = first_name
				user.last_name = last_name
				user.email = email
				user.username = username
				user.save()

				# Then Update Students Table
				student_model = Students.objects.get(users_type=student_id)
				student_model.address = address
				student_model.kcpe_marks = kcpe_marks

				student_class = Classes.objects.get(id=student_class.id)
				student_model.student_class = student_class

				subject_obj = Subjects.objects.get(id=subject_id)
				student_model.students.subject_id =subject_obj

				session_year_obj = SessionYearModel.objects.get(id=session_year_id)
				student_model.session_year_id = session_year_obj

				student_model.gender = gender
				if profile_pic_url != None:
					student_model.profile_pic = profile_pic_url
				student_model.save()
				# Delete student_id SESSION after the data is updated
				del request.session['student_id']

				messages.success(request, "Student Updated Successfully!")
				return redirect('/edit_student/'+student_id)
			except:
				messages.success(request, "Failed to Uupdate Student.")
				return redirect('/edit_student/'+student_id)
		else:
			return redirect('/edit_student/'+student_id)


def delete_student(request, student_id):
	student = Students.objects.get(users_type=student_id)
	try:
		student.delete()
		messages.success(request, "Student Deleted Successfully.")
		return redirect('manage_student')
	except:
		messages.error(request, "Failed to Delete Student.")
		return redirect('manage_student')


def add_subject(request):
	classess = Classes.objects.all()
	staffs = CustomUser.objects.filter(user_type='2')
	context = {
		"classess": classess,
		"staffs": staffs
	}
	return render(request, 'admin_templates/add_subject_template.html', context)



def add_subject_save(request):
	if request.method != "POST":
		messages.error(request, "Method Not Allowed!")
		return redirect('add_subject')
	else:
		form = addSubjectForm(request.POST, request.FILES)
		if form.is_valid():
			subject_name = form.cleaned_data['subject_name']

			class_id = form.cleaned_data['class_id']
			classes = Classes.objects.get(id=class_id)

			session_id = form.cleaned_data['session_id']
			sessions = SessionYearModel.objects.get(id=session_id)
		
			staff_id = form.cleaned_data['staff_id']
			staff = CustomUser.objects.get(id=staff_id)

		try:
			subject = Subjects(subject_name=subject_name,
							classes=classes,
							session_id=sessions,
							staff_id=staff)
			subject.save()
			messages.success(request, "Subject Added Successfully!")
			return redirect('add_subject')
		except:
			messages.error(request, "Failed to Add Subject!")
			return redirect('add_subject')


def manage_subject(request):
	subjects = Subjects.objects.all()
	context = {
		"subjects": subjects
	}
	return render(request, 'admin_templates/manage_subject_template.html', context)


def edit_subject(request, subject_id):
	request.session['subject_id'] = subject_id

	subject = Subjects.objects.get(id=subject_id)
	classes = Classes.objects.all()
	sessions = SessionYearModel.objects.all()
	staffs = CustomUser.objects.filter(user_type='2')
	form = editSubjectForm()
	form.fields["subject_name"] = subject.subject_name
	form.fields["class_id"] = subject.class_id
	form.fields["session_id"] = subject.session_id
	form.fields["staff_id"] = subject.staff_id

	context = {
		"subject": subject,
		"classes": classes,
		"sessions":sessions,
		"staffs": staffs,
		"id": subject_id
	}
	return render(request, 'admin_templates/edit_subject_template.html', context)


def edit_subject_save(request):
	if request.method != "POST":
		HttpResponse("Invalid Method.")
	else:
		subject_id = request.session.get('subject_id')
		if subject_id == None:
			return redirect('/manage_subject')

		form = editSubjectForm(request.POST, request.FILES)
		if form.is_valid():
			class_id = form.cleaned_data['class_id']
			subject_name = form.cleaned_data['subject_name']
			session_id = form.cleaned_data['session_id']
			staff_id = form.cleaned_data['staff_id']

		try:
			subject = Subjects.objects.get(id=subject_id)
			subject.subject_name = subject_name

			classes = Classes.objects.get(id=class_id)
			subject.class_id = classes

			staff = CustomUser.objects.get(id=staff_id)
			subject.staff_id = staff
			
			
			sessions = SessionYearModel.objects.get(id=session_id)
			subject.session_id = sessions
			
			subject.save()
			del request.session['subject_id']
			messages.success(request, "Subject Updated Successfully.")
			
			return HttpResponseRedirect(reverse("edit_subject",
												kwargs={"subject_id":subject_id}))

		except:
			messages.error(request, "Failed to Update Subject.")
			return HttpResponseRedirect(reverse("edit_subject",
												kwargs={"subject_id":subject_id}))
			



def delete_subject(request, subject_id):
	subject = Subjects.objects.get(id=subject_id)
	try:
		subject.delete()
		messages.success(request, "Subject Deleted Successfully.")
		return redirect('manage_subject')
	except:
		messages.error(request, "Failed to Delete Subject.")
		return redirect('manage_subject')


@csrf_exempt
def check_email_exist(request):
	email = request.POST.get("email")
	user_obj = CustomUser.objects.filter(email=email).exists()
	if user_obj:
		return HttpResponse(True)
	else:
		return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
	username = request.POST.get("username")
	user_obj = CustomUser.objects.filter(username=username).exists()
	if user_obj:
		return HttpResponse(True)
	else:
		return HttpResponse(False)



def student_feedback_message(request):
	feedbacks = FeedBackStudent.objects.all()
	context = {
		"feedbacks": feedbacks
	}
	return render(request, 'admin_templates/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
	feedback_id = request.POST.get('id')
	feedback_reply = request.POST.get('reply')

	try:
		feedback = FeedBackStudent.objects.get(id=feedback_id)
		feedback.feedback_reply = feedback_reply
		feedback.save()
		return HttpResponse("True")

	except:
		return HttpResponse("False")


def staff_feedback_message(request):
	feedbacks = FeedBackStaffs.objects.all()
	context = {
		"feedbacks": feedbacks
	}
	return render(request, 'admin_templates/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_reply(request):
	feedback_id = request.POST.get('id')
	feedback_reply = request.POST.get('reply')

	try:
		feedback = FeedBackStaffs.objects.get(id=feedback_id)
		feedback.feedback_reply = feedback_reply
		feedback.save()
		return HttpResponse("True")

	except:
		return HttpResponse("False")


# def student_leave_view(request):
# 	leaves = LeaveReportStudent.objects.all()
# 	context = {
# 		"leaves": leaves
# 	}
# 	return render(request, 'admin_templates/student_leave_view.html', context)

# def student_leave_approve(request, leave_id):
# 	leave = LeaveReportStudent.objects.get(id=leave_id)
# 	leave.leave_status = 1
# 	leave.save()
# 	return redirect('student_leave_view')


# def student_leave_reject(request, leave_id):
# 	leave = LeaveReportStudent.objects.get(id=leave_id)
# 	leave.leave_status = 2
# 	leave.save()
# 	return redirect('student_leave_view')


def staff_leave_view(request):
	leaves = LeaveReportStaff.objects.all()
	context = {
		"leaves": leaves
	}
	return render(request, 'admin_templates/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
	leave = LeaveReportStaff.objects.get(id=leave_id)
	leave.leave_status = 1
	leave.save()
	return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
	leave = LeaveReportStaff.objects.get(id=leave_id)
	leave.leave_status = 2
	leave.save()
	return redirect('staff_leave_view')


def users_type_view_attendance(request):
	subjects = Subjects.objects.all()
	session_years = SessionYearModel.objects.all()
	context = {
		"subjects": subjects,
		"session_years": session_years
	}
	return render(request, "admin_templates/users_type_view_attendance.html", context)


@csrf_exempt
def users_type_get_attendance_dates(request):
	
	subject_id = request.POST.get("subject")
	session_year = request.POST.get("session_year_id")

	# Students enroll to Course, Course has Subjects
	# Getting all data from subject model based on subject_id
	subject_model = Subjects.objects.get(id=subject_id)

	session_model = SessionYearModel.objects.get(id=session_year)
	attendance = Attendance.objects.filter(subject_id=subject_model,
										session_year_id=session_model)

	# Only Passing Student Id and Student Name Only
	list_data = []

	for attendance_single in attendance:
		data_small={"id":attendance_single.id,
					"attendance_date":str(attendance_single.attendance_date),
					"session_year_id":attendance_single.session_year_id.id}
		list_data.append(data_small)

	return JsonResponse(json.dumps(list_data),
						content_type="application/json",
						safe=False)


@csrf_exempt
def users_type_get_attendance_student(request):

	# Getting Values from Ajax POST 'Fetch Student'
	attendance_date = request.POST.get('attendance_date')
	attendance = Attendance.objects.get(id=attendance_date)

	attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
	# Only Passing Student Id and Student Name Only
	list_data = []

	for student in attendance_data:
		data_small={"id":student.student_id.users_type.id,
					"name":student.student_id.users_type.first_name+" "+student.student_id.users_type.last_name,
					"status":student.status}
		list_data.append(data_small)

	return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
	user = CustomUser.objects.get(id=request.user.id)
	form = adminUpdateProfileForm()
	form.fields["username"].initial = user.users_type.username
	form.fields["first_name"].initial = user.users_type.first_name
	form.fields["last_name"].initial = user.users_type.last_name
	form.fields["password"].initial = user.users_type.password
	form.fields["email"].initial = user.users_type.email
	form.fields["profile_pic"].initial = user.users_type.profile_pic

	context={
		"user": user,
		"form":form
	}
	return render(request, 'admin_templates/admin_profile.html', context)


def admin_profile_update(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method!")
		return redirect('admin_profile')
	else:
		form = adminUpdateProfileForm(request.POST, request.FILES)
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

			admin = Admin.objects.get(users_type=customuser.id)
			admin.address = address
			admin.profile_pic = profile_pic
			customuser.save()
			messages.success(request, "Profile Updated Successfully")
			return redirect('admin_profile')
		except:
			messages.error(request, "Failed to Update Profile")
			return redirect('admin_profile')
	


def staff_profile(request):
	pass


def student_profile(requtest):
	pass
