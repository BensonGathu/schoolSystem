from django import forms
from django.forms import ModelForm
from .models import  CustomUser, SessionYearModel, StudentResult, Admin, Staffs, FeedBackStaffs, NotificationStaffs, Classes, Subjects, Students, StudentResult, FeedBackStudent, NotificationStudent, Timetable, Exams
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput




class CreateUserForm(UserCreationForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Enter firstname','type':'text'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={"class":'form-control my-2', 'placeholder':'Enter lastname','type':'text'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter email','type':'email'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Enter password','type':'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Confirm password','type':'password'}))
    class Meta:
        model = CustomUser
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
                        
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))


    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))


    password = forms.CharField(label="Password",
                               max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))


    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))

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

class editStaffForm(forms.Form):
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
                        
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))


    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))


    password = forms.CharField(label="Password",
                               max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))


    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))

    national_ID = forms.IntegerField(label="national_ID",
                             
                              widget=forms.NumberInput(attrs={"class": "form-control"}))

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


class AddStudentForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
                        
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))


    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))


    password = forms.CharField(label="Password",
                               max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))


    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    student_ID = forms.CharField(label="student_ID",
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
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    



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

    class Meta:
        model = Students
        fields = '__all__'

class EditStudentForm(forms.ModelForm):

    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
                        
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))


    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))


    password = forms.CharField(label="Password",
                               max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))


    address = forms.CharField(label="Address",
                              max_length=50,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    student_ID = forms.CharField(label="student_ID",
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
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    
  


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
    class Meta:
        model = Students
        fields = '__all__'


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
        teachers = CustomUser.objects.filter(user_type='2')
        print(teachers)
        teachers_list = []
        for teacher in teachers:
            single_teacher = (teacher.id, teacher.username)
            teachers_list.append(single_teacher)

        print("available teachers",teachers_list)
        
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
class addSubjectForm(forms.Form):
    subject_name =   forms.ChoiceField(label="Subjects",
                                   choices=subject_names,widget=forms.Select(attrs={"class": "form-control"}))


      # For Displaying Classess
    try:
        allclasses = Classes.objects.all()
        classes_list = []
        for classess in allclasses:
            single_class = (classess.id, classess.name, classess.session)
            classes_list.append(single_class)
    except:
        
        classes_list = []
    class_id = forms.ChoiceField(choices=classes_list,widget=forms.Select(attrs={"class": "form-control"}))
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(
                session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []
    session_id =   forms.ChoiceField(label="Session",choices=session_year_list,widget=forms.Select(attrs={"class": "form-control"}))

    try:
        teachers = CustomUser.objects.filter(users_type=2)
        teachers_list = []
        for teacher in teachers:
            teachers_list.append(teacher)
        
    except:
        teachers_list = []

    staff_id =  forms.ChoiceField(label="Teacher",
                                   choices=teachers_list
,
                                   widget=forms.Select(attrs={"class": "form-control"}))



class editSubjectForm(forms.Form):
    subject_name =   forms.ChoiceField(label="Subjects",
                                   choices=subject_names,widget=forms.Select(attrs={"class": "form-control"}))


      # For Displaying Classess
    try:
        allclasses = Classes.objects.all()
        classes_list = []
        for classess in allclasses:
            single_class = (classess.id, classess.name, classess.session)
            classes_list.append(single_class)
    except:
      
        classes_list = []
    class_id = forms.ChoiceField(choices=classes_list,widget=forms.Select(attrs={"class": "form-control"}))
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(
                session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []
    session_id =   forms.ChoiceField(label="Session",choices=session_year_list,widget=forms.Select(attrs={"class": "form-control"}))

    try:
        teachers = CustomUser.objects.filter(users_type=2)
        teachers_list = []
        for teacher in teachers:
            teachers_list.append(teacher)
        
    except:
        teachers_list = []

    staff_id =  forms.ChoiceField(label="Teacher",
                                   choices=teachers_list
,
                                   widget=forms.Select(attrs={"class": "form-control"}))



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
    start_leave_date = forms.DateField(label="start_leave_date",widget=forms.SelectDateWidget())
    end_leave_date = forms.DateField(label="end_leave_date",widget=forms.SelectDateWidget())
    leave_message = forms.CharField(label="leave_message",
                               max_length=500,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))



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







