from django import forms
from .models import  CustomUser, SessionYearModel, StudentResult, Admin, Staffs, FeedBackStaffs, NotificationStaffs, Classes, Subjects, Students, StudentResult, FeedBackStudent, NotificationStudent, Timetable, Exams

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


class AddStudentForm(forms.Form):
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

    # For Displaying Classess
    try:
        allclasses = Classes.objects.all()
        classes_list = []
        for classess in allclasses:
            single_class = (classess.id, classess.name, classess.session)
            classes_list.append(single_class)
    except:
        print("classess here")
        classes_list = []
    # For Displaying Subjects
    try:
        subjects = Subjects.objects.all()
        subject_list = []
        for subject in subjects:
            single_subject = (subject.id, subject.subject_name)
            subject_list.append(single_subject)
    except:
        print("subjects here")
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

    subject_id = forms.ChoiceField(label="Course",
                                   choices=subject_list,
                                   widget=forms.Select(attrs={"class": "form-control"}))


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
                              

    # For Displaying Classess
    try:
        allclasses = Classes.objects.all()
        classes_list = []
        for classess in allclasses:
            single_class = (classess.id, classess.name, classess.session)
            classes_list.append(single_class)
    except:
        print("classess here")
        classes_list = []
    # For Displaying Subjects
    try:
        subjects = Subjects.objects.all()
        subject_list = []
        for subject in subjects:
            single_subject = (subject.id, subject.subject_name)
            subject_list.append(single_subject)
    except:
        print("subjects here")
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

    class_id = forms.ChoiceField(label="Course",
                                   choices=classes_list,
                                   widget=forms.Select(attrs={"class": "form-control"}))

    subject_id = forms.ChoiceField(label="Course",
                                   choices=subject_list,
                                   widget=forms.Select(attrs={"class": "form-control"}))


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

class addSessionYearModelForm(forms.Form):
    session_start_year = forms.DateField(label="session_start_year",widget=forms.SelectDateWidget())
    session_end_year  = forms.DateField(label="session_start_year",widget=forms.SelectDateWidget())

class editSessionYearModelForm(forms.Form):
    session_start_year = forms.DateField(label="session_start_year",widget=forms.SelectDateWidget())
    session_end_year  = forms.DateField(label="session_start_year",widget=forms.SelectDateWidget())


class_list =(
    ("Form One", "Form One"),
    ("Form Two", "Form Two"),
    ("Form Three", "Form Three"),
    ("Form Four ","Form Four"),
)

class addClassForm(forms.Form):
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
        teachers = CustomUser.objects.filter(user_type='2')
        teachers_list = []
        for teacher in teachers:
            teachers_list.append(teacher)
        
    except:
        teachers_list = []
    class_teacher =   forms.ChoiceField(label="Course",
                                   choices=teachers_list
,
                                   widget=forms.Select(attrs={"class": "form-control"})) 



class editClassForm(forms.Form):
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
        print("classess here")
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
        print("classess here")
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







