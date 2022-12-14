from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date


# Create your models here.

terms = (
    ("First Term", "First Term"),
    ("Second Term","Second Term"),
    ("Third Term","Third Term"),

    )  

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    school_term = models.CharField(choices=terms,max_length=100)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    current = models.BooleanField(default=False)
    objects = models.Manager()


    def __str__(self):
        return '{}  {} to {} '.format(self.school_term, self.session_start_year , self.session_end_year)

    

    class Meta:
        unique_together=("school_term", "session_start_year", "session_end_year")


# class CustomUser(AbstractUser):
#     ADMIN = '1'
#     TEACHER = '2'
#     STAFF = '3'
#     STUDENT = '4'
     
#     EMAIL_TO_USER_TYPE_MAP = {
#         'admin': ADMIN,
#         'teacher':TEACHER,
#         'staff': STAFF,fst
#         'student': STUDENT
#     }
 
#     user_type_data = ((ADMIN, "ADMIN"),(TEACHER, "TEACHER"), (STAFF, "Staff"), (STUDENT, "Student"))
#     user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class User(AbstractUser):

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=60, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

    @classmethod
    def get_profile(cls, search_profile):
        profile = cls.objects.filter(first_name__icontains=search_profile)
        return profile
genders = (
    ("Male", "Male"),
    ("Female","Female"),

    ) 
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    users_type = models.OneToOneField(User, on_delete=models.DO_NOTHING, null = True)
    national_ID = models.IntegerField(blank=True,null=True)
    staff_ID = models.TextField(blank=True,null=True)
    gender = models.CharField(choices=genders,max_length=100)
    profile_pic = models.FileField(null=True,blank=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.users_type.username

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    users_type = models.OneToOneField(User, on_delete=models.DO_NOTHING, null = True)
    address = models.TextField()
    national_ID = models.IntegerField()
    staff_ID = models.CharField(max_length=250)
    gender = models.CharField(choices=genders,max_length=100)
    profile_pic = models.FileField(blank=True,null=True)
    phone = models.IntegerField()
    joined_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.users_type.username

class leave_types(models.Model):
    name =  models.CharField(max_length=250)
    def __str__(self):
        return self.name


class LeaveReportStaff(models.Model):  
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(leave_types, on_delete=models.CASCADE)
    start_leave_date = models.DateTimeField()
    end_leave_date = models.DateTimeField()
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return "{}'s  Leave ".format(self.staff_id.users_type.username)

class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


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

class_list =(
    ("Form One", "Form One"),
    ("Form Two", "Form Two"),
    ("Form Three", "Form Three"),
    ("Form Four ","Form Four"),
)

class Classes(models.Model):
    id =models.AutoField(primary_key=True)
    name = models.CharField(choices=class_list,max_length=1000)
    sessionperiod = models.ForeignKey(SessionYearModel,on_delete=models.DO_NOTHING,null = True,blank=True)
    class_teacher = models.ForeignKey(User,on_delete=models.DO_NOTHING, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self): 
        return '{} {}'.format(self.name, self.sessionperiod)


    class Meta:
        unique_together=("name", "sessionperiod_id")

class Subjects(models.Model):
    id =models.AutoField(primary_key=True)
    subject_name = models.CharField(choices=subject_names,max_length=255)
      
    # need to give default course
    class_id = models.ForeignKey(Classes,on_delete=models.DO_NOTHING,null=True)
    # session_id = models.ForeignKey(SessionYearModel, on_delete=models.DO_NOTHING, null = True)
    staff_id = models.ForeignKey(User,on_delete=models.DO_NOTHING, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    def __str__(self):
        return "{} {}".format(self.subject_name,self.class_id)
 
class Students(models.Model):
    id = models.AutoField(primary_key=True)
    users_type = models.OneToOneField(User,on_delete=models.DO_NOTHING, default=1)
    gender = models.CharField(choices=genders,max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    student_id = models.CharField(max_length=150)
    student_class = models.ForeignKey(Classes,on_delete=models.DO_NOTHING,null=True)
    subject_id = models.ManyToManyField(Subjects)
    session_year_id = models.ForeignKey(SessionYearModel, null=True,blank=True,on_delete=models.DO_NOTHING)
    kcpe_marks = models.IntegerField(default=0,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admitted_at = models.DateTimeField(auto_now=True)
    fathers_name = models.CharField(max_length=250)
    fathers_number = models.IntegerField()
    fathers_email = models.EmailField(max_length=250)
    mothers_name = models.CharField(max_length=250)
    student_house = models.CharField(max_length=250)
    mothers_number = models.IntegerField()
    mothers_email = models.EmailField(max_length=250)
    residential_address = models.CharField(max_length=250)
    objects = models.Manager()

    def __str__(self):
        return "{} {} ID = {}".format(self.users_type.first_name,self.users_type.last_name,self.student_id)



class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    classes_id = models.ForeignKey(Classes,on_delete=models.CASCADE)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING,null=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING, null=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.DO_NOTHING, null=True)
    subject_exam1_marks = models.FloatField(validators=[MaxValueValidator(30),MinValueValidator(0)],default=0,null=True,blank=True)
    subject_exam2_marks = models.FloatField(validators=[MaxValueValidator(30),MinValueValidator(0)],default=0,null=True,blank=True)
    subject_endexam_marks = models.FloatField(validators=[MaxValueValidator(70),MinValueValidator(0)],default=0,null=True,blank=True)

 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    

    class Meta:
        unique_together=("student_id", "subject_id")

    def __str__(self):
        if self.subject_exam1_marks != None and self.subject_exam2_marks != None and self.subject_endexam_marks != None:
            return "{} {} = {}".format(self.student_id,self.subject_id,(self.subject_exam1_marks + self.subject_exam2_marks)/2 + self.subject_endexam_marks)
        return "{} results".format(self.student_id)

    @property
    def mean_marks(self):
        if self.subject_exam1_marks != None and self.subject_exam2_marks != None and self.subject_endexam_marks != None:
            return (self.subject_exam1_marks + self.subject_exam2_marks)/2 + self.subject_endexam_marks
        

        elif self.subject_exam1_marks != None and self.subject_exam2_marks == None and self.subject_endexam_marks == None:
            return (self.subject_exam1_marks + 0)/2 + 0

        elif self.subject_exam1_marks != None and self.subject_exam2_marks != None and self.subject_endexam_marks == None:
            return (self.subject_exam1_marks + self.subject_exam2_marks)/2 + 0

        return 0

    @property
    def grade(self):
        if self.subject_exam1_marks != None and self.subject_exam2_marks != None and self.subject_endexam_marks != None:

            gde =(self.subject_exam1_marks + self.subject_exam2_marks)/2 + self.subject_endexam_marks
        
            if 80 <= gde <= 100:
                return "A"
            elif gde >= 75:
                return "A-"
            elif gde >= 70:
                return "B+"
            elif gde >= 65:
                return "B"
            elif gde >= 60:
                return "B-"
            elif gde >= 55:
                return "C+"
            elif gde >= 50:
                return "C"
            elif gde >= 45:
                return "C-"
            elif gde >= 40:
                return "D+"
            elif gde >= 35:
                return "D"
            elif gde >= 30:
                return "D-"
            elif  gde >= 0:
                return "E"
        return "--"

    @property
    def points(self):
        grade = self.grade
        if grade == "A":
            return 12
        elif grade == "A-":
            return 11
        elif grade == "B+":
            return 10
        elif grade == "B":
            return 9
        elif grade == "B-":
            return 8
        elif grade == "C+":
            return 7
        elif grade == "C":
            return 6
        elif grade == "C-":
            return 5
        elif grade == "D+":
            return 4
        elif grade == "D":
            return 3
        elif grade == "D-":
            return 2
        elif grade == "E":
            return 1

class studentReport(models.Model):
    sessionperiod = models.ForeignKey(SessionYearModel,on_delete=models.DO_NOTHING,null = True,blank=True)
    classes_id = models.ForeignKey(Classes,on_delete=models.CASCADE,related_name="class_report")
    student_id = models.ForeignKey(Students,on_delete=models.CASCADE,related_name="student_report")
    all_subjects = models.ManyToManyField(StudentResult)
    date_created = models.DateTimeField(auto_now_add=True)
    p_comments = models.CharField(max_length=100,null=True,blank=True)
    t_comments = models.CharField(max_length=100,null=True,blank=True)
    total_marks = models.FloatField(blank=True,null=True)
    position = models.IntegerField(blank=True,null=True)
    s_mean_marks = models.IntegerField(blank=True,null=True)
    all_points = models.FloatField(blank=True,null=True)

    class Meta:
        unique_together=("sessionperiod","classes_id", "student_id")

    @property
    def get_student_kcpe(self):
        return (self.student.kcpe_marks)/500 * 100

    @property
    def get_Deviation(self):
        if self.get_student_kcpe > self.s_mean_marks:
            return "-{}%".format(abs(self.get_student_kcpe-self.s_mean_marks))
        else:
            return "+{}%".format(abs(self.get_student_kcpe-self.s_mean_marks))


    @property
    def overall_grade(self):
        if self.all_points == 12 :
            return "A"
        elif self.all_points >= 11:
            return "A-"
        elif self.all_points >= 10:
            return "B+"
        elif self.all_points >= 9:
            return "B"
        elif self.all_points >= 8:
            return "B-"
        elif self.all_points >= 7:
            return "C+"
        elif self.all_points >= 6:
            return "C"
        elif self.all_points >= 5:
            return "C-"
        elif self.all_points >= 4:
            return "D+"
        elif self.all_points >= 3:
            return "D"
        elif self.all_points >= 2:
            return "D-"
        elif self.all_points >= 0:
            return "E"

    # def mean(self):
    #     # marks = 0
    #     # for mark in self.all_subjects:
    #     #     marks += mark
    #     # return marks/self.get_number_of_elements()
    #     # return self.objects.all().aggregate(Avg('all_subjects'))
    #     #return self.all_subjects.add()
    #     pass




    def __str__(self):
        return "{} - {}".format(self.student_id,self.classes_id)


    @classmethod
    def filter_by_class(cls,classes_ID):
        report = cls.objects.filter(loc__classes_id=classes_ID).all()
        return report

class subjectInfo(models.Model):
    student_id = models.ForeignKey(Students,on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    position = models.IntegerField(blank=True,null=True)
    mean_marks = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return "{} {} {}".format(self.student_id,self.subject_id,self.position)

    def savesubjectinfo(self):
        self.save()

    class Meta:
        unique_together=("student_id","subject_id")


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()






class Timetable(models.Model):
    pass

class Exams(models.Model):
    pass


# @receiver(post_save, sender=User)
# # Now Creating a Function which will
# # automatically insert data in HOD, Staff or Student
# def create_user_profile(sender, instance, created, **kwargs):
#     # if Created is true (Means Data Inserted)
#     if created:
       
#         # Check the user_type and insert the data in respective tables
#         if instance.user_type == 1:
#             Admin.objects.create(users_type=instance,national_ID=0,address="",staff_ID="",gender="",profile_pic="")
#         if instance.user_type == 2:
#             Staffs.objects.create(users_type=instance,national_ID=0,address="",staff_ID="",gender="",profile_pic="")
#         if instance.user_type == 3:
#             Staffs.objects.create(users_type=instance,national_ID=0,address="",staff_ID="",gender="",profile_pic="")
#         if instance.user_type == 4:
#             Students.objects.create(users_type=instance,
#                                     subject_id="",
#                                     session_year_id="",
#                                     student_class="",
#                                     address="",
#                                     student_id="",
#                                     profile_pic="",
#                                     gender="")
     
 
# @receiver(post_save, sender=CustomUser)
# def save_user_profile(sender, instance, **kwargs):
#     if instance.user_type == 1:
#         instance.admin.save()
#     if instance.user_type == 2:
#         instance.staffs.save()
#     if instance.user_type == 3:
#         instance.students.save()








