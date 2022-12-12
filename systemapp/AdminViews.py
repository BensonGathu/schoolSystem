from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json

from .forms import AddStudentForm, CreateUserForm, EditStudentForm,addClassForm,editClassForm,addSessionYearModelForm,editSessionYearModelForm,addSubjectForm,editSubjectForm,addLeaveReportStaff,addFeedBackStaffs,addNotificationStaffs,addStaffForm,editStaffForm,adminUpdateProfileForm,TeacherSignUpForm,StudentSignUpForm,AdminSignUpForm,TeacherProfileUpdateForm

from .models import User, SessionYearModel, StudentResult, Staffs, FeedBackStaffs, NotificationStaffs, Classes, Subjects, Students, StudentResult, FeedBackStudent, NotificationStudent, Timetable, Exams,LeaveReportStaff,Admin

def teacher_registration(request):
	form = TeacherSignUpForm()
	pform = TeacherProfileUpdateForm()
	if request.method == 'POST':
		form = TeacherSignUpForm(request.POST)
		pform = TeacherProfileUpdateForm(request.POST,request.FILES)
		if form.is_valid() and pform.is_valid():
			form.save()
			print("all data saved")

		else:
			form = TeacherSignUpForm()
			pform = TeacherProfileUpdateForm()
			print("not all data saved")
		context = {
			'form': form,
			'pform':pform
		}
	
	context = {
		'form': form,
		'pform':pform
	}
	return render(request, 'Admin_templates/add_teacher.html', context)


# def add_staff(request):
# 	if request.method == "POST":
# 		first_name = request.POST.get('first_name')
# 		last_name = request.POST.get('last_name')
# 		username = request.POST.get('username')
# 		email = request.POST.get('email')
# 		password = request.POST.get('password')
# 		address = request.POST.get('address')
		
# 		try:
# 			user = User.objects.create_user(username=username,
# 				password=password,email=email,is_staff = True,is_teacher = True,first_name=first_name,last_name=last_name)
# 			user.save()
# 			user.staffs.address = address
# 			user.save()
# 			messages.success(request, "Staff Added Successfully!")
# 			return redirect('add_staff')

# 		except:
# 			messages.error(request, "Failed to Add Staff!")
# 			return redirect('add_staff')
 
	#managing session periods
def manage_session(request):
	session_years = SessionYearModel.objects.all().order_by('-current')
	context = {
		"session_years": session_years
	}
	return render(request, "Admin_templates/manage_session_template.html", context)

 
def add_session(request):
	form = addSessionYearModelForm()
	if request.method == "POST":
		
		form = addSessionYearModelForm(request.POST, request.FILES)
		if form.is_valid():
			print("form is valid ")
			selected_term = form.cleaned_data['school_term']
			session_start_year = form.cleaned_data['session_start_year']
			session_end_year = form.cleaned_data['session_end_year']

		try:
			sessionyear = SessionYearModel(school_term=selected_term,session_start_year=session_start_year,
										session_end_year=session_end_year)
			sessionyear.save()
			messages.success(request, "Session Year added Successfully!")
			return redirect("school:add_session")
		except:
			print("form is invalid ")
			messages.error(request, "Failed to Add Session Year")
			return redirect("school:add_session")
	else:
		form = addSessionYearModelForm()
	context = {
		"form":form
	}
	return render(request, "Admin_templates/add_session_template.html",context)


def edit_session(request, session_id):
	session_year = SessionYearModel.objects.get(id=session_id)
	form = editSessionYearModelForm(request.POST, request.FILES,instance=session_year)

	if request.method == "POST":
		print(" it is a ggggggggggggggggpost")
		form = editSessionYearModelForm(request.POST, request.FILES,instance=session_year)
		
		if form.is_valid():
			print("for is valid")
			form.save()
			return HttpResponseRedirect(request.POST, request.FILES,request.path_info)
		else:
			print("form is invalid")
			form = editSessionYearModelForm(request.POST, request.FILES,instance=session_year)
			context ={
				"form":form
			}
			
			return render(request, "Admin_templates/edit_session_template.html", context)
	
			
	context= {
				"form":form
			}
	return render(request, "Admin_templates/edit_session_template.html", context)




def delete_session(request, session_id):
	session = SessionYearModel.objects.get(id=session_id)
	try:
		session.delete()
		messages.success(request, "Session Deleted Successfully.")
		return redirect('school:manage_session')
	except:
		messages.error(request, "Failed to Delete Session.")
		return redirect('school:manage_session')


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
		"room_name":"broadcast",
	}
	return render(request, "Admin_templates/admin-dashboard.html", context)


# def add_staff_save(request):
# 	form = addStaffForm()
# 	context = {
# 		"form": form
# 	}
# 	return render(request, "admin_templates/add_staff_template.html", context)


def add_staff(request):
	if request.method == "POST":
		form = addStaffForm(request.POST, request.FILES)
		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			address = form.cleaned_data['address']
			staff_ID = form.cleaned_data['staff_ID']
			national_ID = form.cleaned_data['national_ID']
			phonenumber = form.cleaned_data['phone']
			gender = form.cleaned_data['gender']
			joining_date = form.cleaned_data['joining_date']
			
			
			if len(request.FILES) != 0:
				profile_pic = request.FILES['profile_pic']
				fs = FileSystemStorage()
				filename = fs.save(profile_pic.name, profile_pic)
				profile_pic_url = fs.url(filename)
			else:
				profile_pic_url = None

			
			try:
				user = User.objects.create_user(username=email,
													email=email,
													first_name=first_name,
													last_name=last_name,
													password=email,is_staff = True,is_teacher = True,
													)


				user.save()
				teacher = Staffs.objects.create(users_type=user,address=address,national_ID=national_ID,staff_ID=staff_ID,gender=gender,phone=phonenumber,joined_at=joining_date,profile_pic=profile_pic_url)
				
				
				# if profile_pic_url != None:
				# 	teacher.profile_pic = profile_pic_url
				teacher.save()
				print(user)
				messages.success(request, "Staff Added Successfully!")
				return redirect('school:add_staff')
			except:
				 
				messages.error(request, "Failed to Add Staff!")
				return redirect('school:add_staff')
	else:
		form = addStaffForm()
		context = {
		"form": form
		}
		return render(request, "Admin_templates/add_teacher.html", context)



def manage_staff(request):
	staffs = Staffs.objects.all()
	context = {
		"staffs": staffs
	}
	return render(request, "admin_templates/manage_staff_template.html", context)


def edit_staff(request, staff_id):
	teacher_obj = Staffs.objects.get(id=staff_id)
	print(teacher_obj)
	form = editStaffForm(request.POST, request.FILES,instance=teacher_obj)
	if request.method == 'POST':
		form = editStaffForm(request.POST, request.FILES,instance=teacher_obj)

		if form.is_valid():
			form.save()
	
			messages.success(request, "Student Updated Successfully!")
			return redirect('/edit_teacher/'+staff_id)
		else:
			return redirect('/edit_teacher/'+staff_id)
	else:
		print("not post")
		teacher_obj = Staffs.objects.get(id=staff_id)
		print(teacher_obj)
		form = editStaffForm(request.POST, request.FILES,instance=teacher_obj)
		context= {
			"form":form
		}

		return render(request, "Admin_templates/edit_teacher.html", context)



def delete_staff(request, staff_id):
	staff = Staffs.objects.get(users_type=staff_id)
	try:
		staff.delete()
		messages.success(request, "Staff Deleted Successfully.")
		return redirect('manage_staff')
	except:
		messages.error(request, "Failed to Delete Staff.")
		return redirect('manage_staff')


def add_teacher_save(request):
	form = addStaffForm()
	context = {
		"form": form
	}
	return render(request, "admin_templates/add_staff_template.html", context)


def add_teacher(request):
	if request.method != "POST":
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
	else:
		form = addStaffForm()
		context = {
		"form": form
		}
		return render(request, "admin_templates/add_staff_template.html", context)


def manage_teacher(request):
	staffs = Staffs.objects.all()
	context = {
		"staffs": staffs
	}
	return render(request, "Admin_templates/manage_teachers.html", context)



def teacher_view(request,teacher_id):
	teacher = get_object_or_404(Staffs,id=teacher_id)
	
	context = {
		"teacher":teacher
	}
	return render(request, 'Admin_templates/teacher_details.html', context)



def edit_teacher(request,staff_id):
	teacher_obj = Staffs.objects.get(id=staff_id)
	print(teacher_obj)
	form = editStaffForm(request.POST, request.FILES,instance=teacher_obj)
	if request.method == 'POST':
		form = editStaffForm(request.POST, request.FILES,instance=teacher_obj)

		if form.is_valid():
			form.save()
	
			messages.success(request, "Student Updated Successfully!")
			return redirect('/edit_teacher/'+staff_id)
		else:
			return redirect('/edit_teacher/'+staff_id)
	else:
		print("not post")
		student_obj = Students.objects.get(id=staff_id)
		print(student_obj)
		form = editStaffForm(request.POST, request.FILES,instance=teacher_obj)
		context= {
			"form":form
		}

		return render(request, "Admin_templates/edit_teacher.html", context)




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
	form = addSessionYearModelForm()
	
	if request.method == "POST":
		print("its a post")
		form = addClassForm(request.POST, request.FILES)
		
		if form.is_valid():
			name =  form.cleaned_data["name"]
			sessionperiod = form.cleaned_data["sessionperiod"]
			class_teacher = form.cleaned_data["class_teacher"]
			print(class_teacher)
			selected_session = SessionYearModel.objects.get(id=sessionperiod)
			selected_class_teacher = CustomUser.objects.get(id=class_teacher)
			print("selected_session",selected_session)
			print("selected_class_teacher",selected_class_teacher)
			new_class = Classes(
				name=name,
				sessionperiod_id='Third Term 2023-09-04 to 2023-12-04',
				class_teacher=selected_class_teacher
			)
			new_class.save()
			
			messages.success(request, "Class Added Successfully!")
			return redirect('school:add_class')
		
		messages.error(request, "Failed to Add Class!")
		return redirect('school:add_class')
	else:
		form = addClassForm()

		context = {"form":form}
		return render(request, "Admin_templates/add_class_template.html",context)


def manage_class(request):
	classes = Classes.objects.all()
	context = {
		"classes": classes
	}
	return render(request, 'Admin_templates/manage_classes.html', context)

def previous_class(request):
	classes = Classes.objects.all()
	context = {
		"classes": classes
	}
	return render(request, 'Admin_templates/previous_classes.html', context)


# def edit_class_save(request, class_id):
# 	classes = Classes.objects.get(id=class_id)

# 	#adding class ID  into session variable
# 	request.session["class_id"] = class_id

# 	form = editClassForm()
	
# 	# Filling the form with Data from Database
# 	form.fields["name"]=classes.name
# 	form.fields["sessionperiod"]=classes.sessionperiod
# 	form.fields["class_teacher"]=classes.class_teacher
# 	context = {
# 		"classes": classes,
# 		"id": class_id,
# 		"form":form
# 	}

# 	return render(request, 'admin_templates/edit_class_template.html', context)


def edit_class(request,class_id):
	
	class_prof = get_object_or_404(Classes, id=class_id)
	form = editClassForm(request.POST, request.FILES, instance=class_prof)
	if request.method == "POST":
		print("class post")
		form = editClassForm(request.POST, request.FILES, instance=class_prof)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(request.path_info)

		else:
			form = editClassForm(request.POST, request.FILES, instance=class_prof)

		context = {
			"form":form
		}
		return render(request, 'Admin_templates/edit_classes.html', context)
	context = {
			"form":form
		}
	return render(request, 'Admin_templates/edit_classes.html', context)


def delete_class(request, class_id):
	classes = Classes.objects.get(id=class_id)
	try:
		classes.delete()
		messages.success(request, "Class Deleted Successfully.")
		return redirect('manage_class')
	except:
		messages.error(request, "Failed to Delete class.")
		return redirect('manage_class')





# def add_student(request):
# 	form = AddStudentForm()
# 	context = {
# 		"form": form
# 	}
# 	return render(request, 'add-student.html', context)


def student_view(request,student_id):
	student = get_object_or_404(Students,id=student_id)
	context = {
		"student":student
	}
	return render(request, 'Admin_templates/student_details.html', context)

def studentReg(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            
            first_name = form.cleaned_data['firstname']
            last_name = form.cleaned_data.get('lastname')
            email_id = form.cleaned_data.get('email')
            
            password = form.cleaned_data.get('password1')
            confirm_password = form.cleaned_data.get('password2')


        user_type = get_user_type_from_email(email_id)
        print(user_type)

        if user_type is None:
            messages.error(request, "Please use valid format for the email id: '<username>.<staff|student|hod>@<college_domain>'")
            # return render(request, 'auth/registration.html',context)

        username = email_id.split('@')[0].split('.')[0]
        print(username)

        user = CustomUser()
        user.username = username
        user.email = email_id
        # user.password = password
        user.user_type = user_type
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        

        if user_type == CustomUser.STAFF:
            Staffs.objects.create(users_type=user)
        elif user_type == CustomUser.STUDENT:
            Students.objects.create(users_type=user)
        elif user_type == CustomUser.ADMIN:
            Admin.objects.create(users_type=user)
        elif user_type == CustomUser.TEACHER:
            Staffs.objects.create(users_type=user)
        return redirect("school:doLogin")

    context = {
                            "form": form
        }
    return render(request, 'auth/registration.html', context)


def get_user_type_from_email(email_id):
    """
    Returns CustomUser.user_type corresponding to the given email address
    email_id should be in following format:
    '<username>.<staff|student|hod>@<college_domain>'
    eg.: 'abhishek.staff@jecrc.com'
    """

    try:
        email_id = email_id.split('@')[0]
        email_user_type = email_id.split('.')[1]
        return CustomUser.EMAIL_TO_USER_TYPE_MAP[email_user_type]
    except:
        return None

def add_student(request):
	if request.method == "POST":
		form = AddStudentForm(request.POST, request.FILES)
		if form.is_valid():
			profile_pic= form.cleaned_data['profile_pic']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			student_ID = form.cleaned_data['student_ID']
			student_house = form.cleaned_data['student_house']
			address = form.cleaned_data['address']
			session_year_id = form.cleaned_data['session_year_id']
			class_id = form.cleaned_data['class_id']
			subject_id = form.cleaned_data['subject_id']
			kcpe_marks = form.cleaned_data['kcpe_marks']
			gender = form.cleaned_data['gender']
			fathers_name = form.cleaned_data['fathers_name']
			fathers_email = form.cleaned_data['fathers_email']
			fathers_phonenumber =form.cleaned_data['firstfathers_phonenumber_name']
			mothers_name = form.cleaned_data['mothers_name']
			mothers_email = form.cleaned_data['mothers_email']
			mothers_phonenumber = form.cleaned_data['mothers_phonenumber']
			residential_address =form.cleaned_data['residential_address']
			admission_date = form.cleaned_data['admission_date']

		


			try:
				user = User.objects.create_user(username=email,
													password=email,
													email=email,
													first_name=first_name,
													last_name=last_name,
													is_student=True

													)
				student = Students.objects.create(users_type=user,gender=gender,profile_pic=profile_pic,address=address,student_id=student_ID,student_class=class_id,subject_id=subject_obj,session_year_id=session_year_id,kcpe_marks=kcpe_marks,admitted_at=admission_date,fathers_name=fathers_name,fathers_number=fathers_phonenumber,fathers_email=fathers_email,mothers_name=mothers_name,student_house=student_house,mothers_number=mothers_phonenumber,mothers_email=mothers_email,residential_address=residential_address)

				user.students.kcpe_marks =kcpe_marks
				subject_obj = Subjects.objects.get(id=subject_id)
				user.students.subject_id =subject_obj



				user.save()
				messages.success(request, "Student Added Successfully!")
				return HttpResponseRedirect('add_student')
			except:
				
				messages.error(request, "Failed to Add Staff!")
				return redirect('school:add_staff')

	else:

			
		form = AddStudentForm()	
			
		context = {
			'form': form
		}
		print("invalid")
		return render(request, 'Admin_templates/add_student.html', context)


def manage_student(request):
	students = Students.objects.all()
	context = {
		"students": students
	} 
	return render(request, 'Admin_templates/manage_students.html', context)


# def edit_student_save(request, student_id):

# 	# Adding Student ID into Session Variable
# 	request.session['student_id'] = student_id

# 	student = Students.objects.get(users_type=student_id)
# 	form = EditStudentForm()
	
# 	# Filling the form with Data from Database
# 	form.fields['email'].initial = student.users_type.email
# 	form.fields['username'].initial = student.users_type.username
# 	form.fields['first_name'].initial = student.users_type.first_name
# 	form.fields['last_name'].initial = student.users_type.last_name
# 	form.fields['address'].initial = student.address
# 	form.fields['class_id'].initial = student.student_class
# 	form.fields['subject_id'].initial = student.subject_id
# 	form.fields['kcpe_marks'].initial = student.kcpe_marks
# 	form.fields['gender'].initial = student.gender
# 	form.fields['session_year_id'].initial = student.session_year_id

# 	context = {
# 		"id": student_id,
# 		"username": student.users_type.username,
# 		"form": form
# 	}
# 	return render(request, "edit-student.html", context)


def edit_student(request,student_id):
	student_obj = Students.objects.get(id=student_id)
	print(student_obj)
	form = EditStudentForm(request.POST, request.FILES,instance=student_obj)
	if request.method == 'POST':
		form = EditStudentForm(request.POST, request.FILES,instance=student_obj)

		if form.is_valid():
			form.save()
			# profile_pic= request.POST.get('profile_pic')
			# first_name = request.POST.get('first_name')
			# last_name = request.POST.get('last_name')
			# email = request.POST.get('email')
			# student_ID = request.POST.get('student_ID')
			# address = request.POST.get('residential_address')
			# session_year_id = request.POST.get('session_year_id')
			# class_id = request.POST.get('class_id')
			# subject_id = request.POST.get('subject_id')
			# kcpe_marks = request.POST.get('kcpe_marks')
			# gender = request.POST.get('gender')
			# fathers_name = request.POST.get('fathers_name')
			# fathers_email = request.POST.get('fathers_email')
			# fathers_phonenumber = request.POST.get('fathers_phonenumber')
			# mothers_name = request.POST.get('mothers_name')
			# mothers_email = request.POST.get('mothers_email')
			# mothers_phonenumber = request.POST.get('mothers_phonenumber')
			# residential_address = request.POST.get('residential_address')
			# admission_date = request.POST.get('admission_date')


			# Getting Profile Pic first
			# First Check whether the file is selected or not
			# Upload only if file is selected
			# if len(request.FILES) != 0:
			# 	profile_pic = request.FILES['profile_pic']
			# 	fs = FileSystemStorage()
			# 	filename = fs.save(profile_pic.name, profile_pic)
			# 	profile_pic_url = fs.url(filename)
			# else:
			# 	profile_pic_url = None

			# try:
			# 	# First Update into Custom User Model
			# 	user = CustomUser.objects.get(id=student_id)
			# 	user.first_name = first_name
			# 	user.last_name = last_name
			# 	user.email = email
			
			# 	user.save()

			# 	# Then Update Students Table
			# 	student_model = Students.objects.get(users_type=student_id)
			# 	student_model.address = address
			# 	student_model.kcpe_marks = kcpe_marks

			# 	student_class = Classes.objects.get(id=student_class.id)
			# 	student_model.student_class = student_class

			# 	subject_obj = Subjects.objects.get(id=subject_id)
				# student_model.students.subject_id =subject_obj

				# session_year_obj = SessionYearModel.objects.get(id=session_year_id)
				# student_model.session_year_id = session_year_obj
				# student_model.class_id = class_id
				# student_model.admission_date = admission_date
				# student_model.student_ID = student_ID
				# student_model.gender = gender
				# student_model.fathers_name = fathers_name
				# student_model.fathers_email = fathers_email
				# student_model.fathers_phonenumber = fathers_phonenumber
				# student_model.mothers_name = mothers_name
				# student_model.mothers_email = mothers_email
				# student_model.mothers_phonenumber = mothers_phonenumber
				# student_model.residential_address = residential_address
				
				# if profile_pic_url != None:
				# 	student_model.profile_pic = profile_pic_url
				# student_model.save()
			messages.success(request, "Student Updated Successfully!")
			return redirect('/edit_student/'+student_id)
		else:
			return redirect('/edit_student/'+student_id)
	else:
		print("not post")
		student_obj = Students.objects.get(id=student_id)
		print(student_obj)
		form = EditStudentForm(request.POST, request.FILES,instance=student_obj)
		context= {
			"form":form
		}

		return render(request, "Admin_templates/edit_student.html", context)

		

def delete_student(request, student_id):
	student = Students.objects.get(users_type=student_id)
	try:
		student.delete()
		messages.success(request, "Student Deleted Successfully.")
		return redirect('manage_student')
	except:
		messages.error(request, "Failed to Delete Student.")
		return redirect('manage_student')


# def add_subject_save(request):
# 	classess = Classes.objects.all()
# 	staffs = CustomUser.objects.filter(user_type='2')
# 	context = {
# 		"classess": classess,
# 		"staffs": staffs
# 	}
# 	return render(request, 'admin_templates/add_subject_template.html', context)



def add_subject(request):
	form = addSubjectForm(request.POST, request.FILES)
	if request.method == "POST":
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
			return redirect('school:add_subject')
		except:
			messages.error(request, "Failed to Add Subject!")
			return redirect('school:add_subject')

	context = {
		"form": form,
	}

	return render(request, 'Admin_templates/add_subjects.html', context)


def manage_subject(request):
	subjects = Subjects.objects.all()
	context = {
		"subjects": subjects
	}
	return render(request, 'Admin_templates/manage_subjects.html', context)





def edit_subject(request,subject_id):
	subject_obj = Subjects.objects.get(id=subject_id)
	form = editSubjectForm(request.POST, request.FILES,instance=subject_obj)
	if request.method == "POST":
		form = editSubjectForm(request.POST, request.FILES,instance=subject_obj)

		if form.is_valid():
			form.save()
	
			messages.success(request, "Student Updated Successfully!")
			return redirect('school:edit_subject',subject_id)
		else:
			return redirect('school:edit_subject',subject_id)
	else:
		print("not post")
		subject_obj = Subjects.objects.get(id=subject_id)
		print(subject_obj)
		form = editSubjectForm(request.POST, request.FILES,instance=subject_obj)
		context= {
			"form":form
		}

		return render(request, "Admin_templates/edit_subject.html", context)





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
	approved_leaves =LeaveReportStaff.objects.filter(leave_status = 1)
	pending_leaves =LeaveReportStaff.objects.filter(leave_status = 0)
	rejected_leaves =LeaveReportStaff.objects.filter(leave_status = 2)
	context = {
		"leaves": leaves,
		"approved_leaves":approved_leaves,
		"pending_leaves":pending_leaves,
		"rejected_leaves":rejected_leaves	
	}
	return render(request, 'Admin_templates/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
	leave = LeaveReportStaff.objects.get(id=leave_id)
	leave.leave_status = 1
	leave.save()
	return redirect('school:staff_leave_view')


def staff_leave_reject(request, leave_id):
	leave = LeaveReportStaff.objects.get(id=leave_id)
	leave.leave_status = 2
	leave.save()
	return redirect('school:staff_leave_view')


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
