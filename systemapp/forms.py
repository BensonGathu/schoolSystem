from django import forms
from django.forms import ModelForm
from .models import  User, SessionYearModel, StudentResult, Admin, Staffs, FeedBackStaffs, NotificationStaffs, Classes, Subjects, Students,  FeedBackStudent, NotificationStudent, Timetable, Exams,leave_types
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from django.db import transaction 
from bootstrap_modal_forms.forms import BSModalModelForm

class BookModelForm(BSModalModelForm):
    class Meta:
        model = StudentResult
        fields = ['subject_exam1_marks','subject_exam2_marks','subject_endexam_marks']


class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Enter firstname','type':'text'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Enter lastname','type':'text'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter email','type':'email'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter password','type':'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Confirm password','type':'password'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']




    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data.get('email'))
        user.save()
        teacher = Staffs.objects.create(users_type=user)
        
        teacher.save()
        return user


class TeacherProfileUpdateForm(forms.ModelForm):
    national_ID = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Natioanl ID Number','type':'number'}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Enter Address','type':'text'}))
    staff_ID = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter Staff ID','type':'text'}))
    
    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )



    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    phone = forms.IntegerField(label="phonenumber",
                             
                              widget=forms.NumberInput(attrs={"class": "form-control"}))

    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))

    joined_at = forms.DateField(
               widget=forms.TextInput(
               attrs={'type':'date','class': 'form-control'}))


    class Meta:
        model = Staffs
        fields = ['national_ID', 'address', 'staff_ID','gender','phone','profile_pic','joined_at']

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(
        max_length=60, help_text='Required. Inform a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        student = Students.objects.create(user=user)
        student.save()
        return user

class AdminSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(
        max_length=60, help_text='Required. Inform a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        admin = Admin.objects.create(user=user)
        admin.save()
        return user


class CreateUserForm(UserCreationForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Enter firstname','type':'text'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Enter lastname','type':'text'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter email','type':'email'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter password','type':'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Confirm password','type':'password'}))
    class Meta:
        model = User
        fields = ['firstname','lastname','email','password1','password2']


#AdminView Forms
class DateInput(forms.DateInput):
    input_type = "date"

class addStaffForm(forms.Form):
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
                        

    joining_date = forms.DateField(
               widget=forms.TextInput(
               attrs={'type':'date','class': 'form-control'}))
 

    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    phone = forms.IntegerField(label="phonenumber",
                             
                              widget=forms.NumberInput(attrs={"class": "form-control"}))




    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.Textarea(attrs={"class": "form-control",'rows':3,'cols':45}))

    national_ID = forms.IntegerField(label="national_ID",
                              
                              widget=forms.TextInput(attrs={"class": "form-control"}))

    staff_ID = forms.CharField(label="staff_ID",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))

    

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )



    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))


    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


    

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )



    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))


    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


class editStaffForm(forms.Form):
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
                        

    joining_date = forms.DateField(
               widget=forms.TextInput(
               attrs={'type':'date','class': 'form-control'}))
 

    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    phone = forms.IntegerField(label="phonenumber",
                             
                              widget=forms.NumberInput(attrs={"class": "form-control"}))




    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.Textarea(attrs={"class": "form-control",'rows':3,'cols':45}))

    national_ID = forms.IntegerField(label="national_ID",
                              
                              widget=forms.TextInput(attrs={"class": "form-control"}))

    staff_ID = forms.CharField(label="staff_ID",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))

    

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )



    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))


    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))




class AddStudentForm(forms.Form):
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
                        


    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))


    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    admission_date = forms.DateField(
               widget=forms.TextInput(
               attrs={'type':'date','class': 'form-control'}))
    student_ID = forms.CharField(label="student_ID",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    student_house = forms.CharField(label="student House",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    fathers_name = forms.CharField(label="fathers_name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    fathers_email = forms.EmailField(label="fathers_email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    fathers_phonenumber = forms.IntegerField(label="fathers_phonenumber",
                             
                              widget=forms.NumberInput(attrs={"class": "form-control"}))
    
    mothers_name = forms.CharField(label="mothers_name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    mothers_email = forms.EmailField(label="mothers_email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    
    mothers_phonenumber = forms.IntegerField(label="mothers_phonenumber",
                             
                              widget=forms.NumberInput(attrs={"class": "form-control"}))
    
    residential_address = forms.CharField(label="residential_address",
                                max_length=50,
                                widget=forms.Textarea(attrs={"class": "form-control",'rows':3,'cols':40}))

    



    # For Displaying Classess
    try:
        allclasses = Classes.objects.all()
     
        classes_list = []
        for classess in allclasses:
          
            single_class = (classess.id, classess.name)
           
            classes_list.append(single_class)
    except:
       
        classes_list = []

        
    # For Displaying Subjects
    try:
        subjects = Subjects.objects.all()
        subject_list = []
        for subject in subjects:
            single_subject = (subject.id, subject.subject_name)
            subject_list.append(single_subject)
    except:
      
        subject_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:

            single_session_year = (session_year.id, str(
                session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)
       

    except:
        session_year_list = []
   



    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
  

    class_id = forms.ChoiceField(label="Classes",
                                   choices=classes_list,
                                   widget=forms.Select(attrs={"class": "form-control"}))

    subject_id = forms.MultipleChoiceField(label="Course",
                                   choices=subject_list,
                                   widget=forms.SelectMultiple(attrs={"class": "form-control"}))


    session_year_id = forms.ChoiceField(label="Session Year",
                                        choices=session_year_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))

    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))


    kcpe_marks = forms.IntegerField(label="kcpe_marks ",
                                  required=False,
                                  widget=forms.NumberInput(attrs={"class": "form-control"}))

    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


class EditStudentForm(forms.Form): 

    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
                        


    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))


    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    admission_date = forms.DateField(
               widget=forms.TextInput(
               attrs={'type':'date','class': 'form-control'}))
    student_ID = forms.CharField(label="student_ID",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    student_house = forms.CharField(label="student House",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    fathers_name = forms.CharField(label="fathers_name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    fathers_email = forms.EmailField(label="fathers_email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    fathers_phonenumber = forms.IntegerField(label="fathers_phonenumber",
                             
                              widget=forms.NumberInput(attrs={"class": "form-control"}))
    
    mothers_name = forms.CharField(label="mothers_name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    mothers_email = forms.EmailField(label="mothers_email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    
    mothers_phonenumber = forms.IntegerField(label="mothers_phonenumber",
                             
                              widget=forms.NumberInput(attrs={"class": "form-control"}))
    
    residential_address = forms.CharField(label="residential_address",
                                max_length=50,
                                widget=forms.Textarea(attrs={"class": "form-control",'rows':3,'cols':40}))

    



    # For Displaying Classess
    try:
        allclasses = Classes.objects.all()
     
        classes_list = []
        for classess in allclasses:
          
            single_class = (classess.id, classess.name)
           
            classes_list.append(single_class)
    except:
       
        classes_list = []
    # For Displaying Subjects
    try:
        subjects = Subjects.objects.all()
        subject_list = []
        for subject in subjects:
            single_subject = (subject.id, subject.subject_name)
            subject_list.append(single_subject)
    except:
      
        subject_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:

            single_session_year = (session_year.id, str(
                session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)
       

    except:
        session_year_list = []
   



    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
  

    class_id = forms.ChoiceField(label="Classes",
                                   choices=classes_list,
                                   widget=forms.Select(attrs={"class": "form-control"}))

    subject_id = forms.MultipleChoiceField(label="Course",
                                   choices=subject_list,
                                   widget=forms.SelectMultiple(attrs={"class": "form-control"}))


    session_year_id = forms.ChoiceField(label="Session Year",
                                        choices=session_year_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))

    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))


    kcpe_marks = forms.IntegerField(label="kcpe_marks ",
                                  required=False,
                                  widget=forms.NumberInput(attrs={"class": "form-control"}))

    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


terms = (
    ("First Term", "First Term"),
    ("Second Term","Second Term"),
    ("Third Term","Third Term"),

    ) 


class addSessionYearModelForm(forms.ModelForm):
    school_term = forms.ChoiceField(label="Select Term",
                               choices=terms,
                               widget=forms.Select(attrs={"class": "form-control"}))
   
    session_start_year = forms.DateField(
               widget=forms.TextInput(
               attrs={'type':'date','class': 'form-control'}))

    session_end_year  = forms.DateField(
               widget=forms.TextInput(
               attrs={'type':'date','class': 'form-control'}))

    class Meta:
        model = SessionYearModel
        fields = '__all__'
        # widgets = {
        #     'session_start_year': DateInput(),
        #     'session_end_year': DateInput(),
        # }
        
class editSessionYearModelForm(forms.ModelForm):
    school_term = forms.ChoiceField(label="Select Term",
                               choices=terms,
                               widget=forms.Select(attrs={"class": "form-control"}))


       
    session_start_year = forms.DateField(
               widget=forms.TextInput(
               attrs={'type':'date','class': 'form-control'}))

    session_end_year  = forms.DateField(
               widget=forms.TextInput(
               attrs={'type':'date','class': 'form-control'}))
   


    class Meta:
        model = SessionYearModel
        fields = '__all__'


class_list =(
    ("Form One", "Form One"),
    ("Form Two", "Form Two"),
    ("Form Three", "Form Three"),
    ("Form Four ","Form Four"),
)

class addClassForm(forms.ModelForm):
    name = forms.ChoiceField(label="Class Name",choices=class_list,widget=forms.Select(attrs={"class":"form-control"}))

    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = session_year,session_year
            print(session_year)
            session_year_list.append(single_session_year)
             
    except:
        session_year_list = []

    new_sessionlist = []
    
    print("available sessions",session_year_list)
    sessionperiod =  forms.ChoiceField(label="Session",
                                   choices=session_year_list
,
                                 widget=forms.Select(attrs={"class": "form-control my-2"})) 
    
    try:
        teachers = Staffs.objects.all()
        teachers_list = []
        for teacher in teachers:
            single_teacher = (teacher.id, teacher.users_type.username)
            teachers_list.append(single_teacher)


        
    except:
        teachers_list = []
    class_teacher =   forms.ChoiceField(label="Class Teacher",
                                   choices=teachers_list
,
                                   widget=forms.Select(attrs={"class": "form-control my-2"})) 

    class Meta:
        model = Classes
        fields = '__all__'


class editClassForm(forms.ModelForm):
    name = forms.ChoiceField(label="Class Name",choices=class_list,widget=forms.Select(attrs={"class":"form-control"}))

    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(
                session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []
    session =   forms.ChoiceField(label="Course",
                                   choices=session_year_list
,
                                   widget=forms.Select(attrs={"class": "form-control"})) 
    
    try:
        teachers = Staffs.objects.filter(users_type=2)
        teachers_list = []
        for teacher in teachers:
            teachers_list.append(teacher)
        
    except:
        teachers_list = []
    class_teacher =   forms.ChoiceField(label="Course",
                                   choices=teachers_list
,
                                   widget=forms.Select(attrs={"class": "form-control"})) 

    class Meta:
        model = Classes
        fields = '__all__'



subject_names = (
    ("English", "English"),
    ("Mathematics","Mathematics"),
    ("Kiswahili", "Kiswahili"),
    ("Chemistry","Chemistry"),
    ("Physics", "Physics"),
    ("Biology","Biology"),
    ("Geography", "Geography"),
    ("History", "History"),
    ("C.R.E", "C.R.E"),
    ("Agriculture", "Agriculture"),
    ("Business Studies", "Business Studies"),
    )
class addSubjectForm(forms.ModelForm):
    subject_name =   forms.ChoiceField(label="Subjects",
                                   choices=subject_names,widget=forms.Select(attrs={"class": "form-control"}))


      # For Displaying Classess
    try:
        allclasses = Classes.objects.all()
     
        classes_list = []
        for classess in allclasses:
          
            single_class = (classess.id, classess.name)
           
            classes_list.append(single_class)
    except:
        
        classes_list = []
    print("subect classes",classes_list)
    class_id = forms.ChoiceField(choices=classes_list,widget=forms.Select(attrs={"class": "form-control"}))
    # try:
    #     session_years = SessionYearModel.objects.all()
    #     session_year_list = []
    #     for session_year in session_years:
    #         single_session_year = (session_year.id, str(
    #             session_year.session_start_year)+" to "+str(session_year.session_end_year))
    #         session_year_list.append(single_session_year)

    # except:
    #     session_year_list = []

    # print("subect classes",classes_list)
    # session_id =   forms.ChoiceField(label="Session",choices=session_year_list,widget=forms.Select(attrs={"class": "form-control"}))

    try:
        teachers = Staffs.objects.all()
        teachers_list = []
        for teacher in teachers:
            single_teacher = (teacher.id, teacher.users_type.username)
            teachers_list.append(single_teacher)
        
    except:
        teachers_list = []
    print("subject trs",teachers_list)

    staff_id =  forms.ChoiceField(label="Teacher",
                                   choices=teachers_list
,
                                   widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = Subjects
        fields = '__all__'



class editSubjectForm(forms.ModelForm):
    subject_name =   forms.ChoiceField(label="Subjects",
                                   choices=subject_names,widget=forms.Select(attrs={"class": "form-control"}))


      # For Displaying Classess
    try:
        allclasses = Classes.objects.all()
     
        classes_list = []
        for classess in allclasses:
          
            single_class = (classess.id, classess.name)
           
            classes_list.append(single_class)
    except:
        
        classes_list = []
    print("subect classes",classes_list)
    class_id = forms.ChoiceField(choices=classes_list,widget=forms.Select(attrs={"class": "form-control"}))
    # try:
    #     session_years = SessionYearModel.objects.all()
    #     session_year_list = []
    #     for session_year in session_years:
    #         single_session_year = (session_year.id, str(
    #             session_year.session_start_year)+" to "+str(session_year.session_end_year))
    #         session_year_list.append(single_session_year)

    # except:
    #     session_year_list = []

    # print("subect classes",classes_list)
    # session_id =   forms.ChoiceField(label="Session",choices=session_year_list,widget=forms.Select(attrs={"class": "form-control"}))

    try:
        teachers = Staffs.objects.all()
        teachers_list = []
        for teacher in teachers:
            single_teacher = (teacher.id, teacher.users_type.username)
            teachers_list.append(single_teacher)
        
    except:
        teachers_list = []
    print("subject trs",teachers_list)

    staff_id =  forms.ChoiceField(label="Teacher",
                                   choices=teachers_list
,
                                   widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = Subjects
        fields = '__all__'



class adminUpdateProfileForm(forms.Form):
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
                        
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))


    password = forms.CharField(label="Password",
                               max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


class addLeaveReportStaff(forms.Form):
    pass

class addFeedBackStaffs(forms.Form):
    pass

class addNotificationStaffs(forms.Form):
    pass
 


#StaffView Forms
class staffUpdateProfileForm(forms.Form):
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
                        
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))


    password = forms.CharField(label="Password",
                               max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


 
class staffApplyLeaveForm(forms.Form):
    try:
        leave_types = leave_types.objects.all()
        leave_type_list = []
        for leave in leave_types:
            single_leave = (leave.id, leave.name)
            leave_type_list.append(single_leave)

       
        
    except:
        teachers_list = []

    leave_type = forms.ChoiceField(label="Leave Type",
                               choices=leave_type_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    start_leave_date  = forms.DateField(
               widget=forms.TextInput(
               attrs={'type':'date','class': 'form-control'}))
    end_leave_date = forms.DateField(
               widget=forms.TextInput(
               attrs={'type':'date','class': 'form-control'}))
    leave_message = forms.CharField(label="leave_message",
                              max_length=500,
                              widget=forms.Textarea(attrs={"class": "form-control",'rows':3,'cols':45}))




#studentView Forms
class studentUpdateProfileForm(forms.Form):
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
                        
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))


    password = forms.CharField(label="Password",
                               max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))

    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))







#add marks/results form
class addResultsForm(forms.ModelForm):
    subject_exam1_marks = forms.IntegerField(label="Cat one",required=False,
                             
                              widget=forms.NumberInput(attrs={"class": "form-control"}))
    subject_exam2_marks = forms.IntegerField(label="Cat two",required=False,
                             
                              widget=forms.NumberInput(attrs={"class": "form-control"}))
    subject_endexam_marks= forms.IntegerField(label="End term",required=False,
                             
                              widget=forms.NumberInput(attrs={"class": "form-control"}))

    class Meta:
        model = StudentResult
        fields = ['subject_exam1_marks','subject_exam2_marks','subject_endexam_marks']