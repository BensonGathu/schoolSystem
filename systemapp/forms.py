from django import forms
from .models import Courses, SessionYearModel, StudentResult, Admin, Staffs, FeedBackStaffs, NotificationStaffs, Classes, Subjects, Students, StudentResult, FeedBackStudent, NotificationStudent, Timetable, Exams


class DateInput(forms.DateInput):
    input_type = "date"


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


    kcpe_marks = forms.FileField(label="kcpe_marks ",
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


    kcpe_marks = forms.FileField(label="kcpe_marks ",
                                  required=False,
                                  widget=forms.NumberInput(attrs={"class": "form-control"}))

    profile_pic = forms.FileField(label="Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))
