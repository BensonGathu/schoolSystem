from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()





class CustomUser(AbstractUser):
    ADMIN = '1'
    TEACHER = '2'
    STAFF = '3'
    STUDENT = '4'
     
    EMAIL_TO_USER_TYPE_MAP = {
        'admin': ADMIN,
        'teacher':TEACHER,
        'staff': STAFF,
        'student': STUDENT
    }
 
    user_type_data = ((ADMIN, "ADMIN"),(TEACHER, "TEACHER"), (STAFF, "Staff"), (STUDENT, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
 
genders = (
    ("Male", "Male"),
    ("Female","Female"),

    ) 
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    users_type = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING, null = True)
    national_ID = models.IntegerField()
    staff_ID = models.TextField()
    gender = models.CharField(choices=genders,max_length=100)
    profile_pic = models.FileField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    users_type = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING, null = True)
    address = models.TextField()
    national_ID = models.IntegerField()
    staff_ID = models.TextField()
    gender = models.CharField(choices=genders,max_length=100)
    profile_pic = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    start_leave_date = models.CharField(max_length=255)
    end_leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

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
    sessionperiod = models.ForeignKey(SessionYearModel,on_delete=models.DO_NOTHING)
    class_teacher = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    class Meta:
        unique_together=("name", "sessionperiod")

class Subjects(models.Model):
    id =models.AutoField(primary_key=True)
    subject_name = models.CharField(choices=subject_names,max_length=255)
     
    # need to give default course
    class_id = models.ForeignKey(Classes,on_delete=models.DO_NOTHING,null=True)
    session_id = models.ForeignKey(SessionYearModel, on_delete=models.DO_NOTHING, null = True)
    staff_id = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    users_type = models.OneToOneField(CustomUser,on_delete=models.DO_NOTHING, default=1)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    student_id = models.CharField(max_length=150)
    student_class = models.ForeignKey(Classes,on_delete=models.DO_NOTHING,null=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING, null=True)
    session_year_id = models.ForeignKey(SessionYearModel, null=True,
                                        on_delete=models.DO_NOTHING)
    kcpe_marks = models.IntegerField(default=0,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING,null=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING, null=True)
    subject_exam1_marks = models.FloatField(validators=[MaxValueValidator(30),MinValueValidator(0)],default=0)
    subject_exam2_marks = models.FloatField(validators=[MaxValueValidator(30),MinValueValidator(0)],default=0)
    subject_endexam_marks = models.FloatField(validators=[MaxValueValidator(70),MinValueValidator(0)],default=0)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    class Meta:
        unique_together=("student_id", "subject_id")




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


@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will
# automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
       
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Admin.objects.create(users_type=instance,national_ID=0,address="",staff_ID="",gender="",profile_pic="")
        if instance.user_type == 2:
            Staffs.objects.create(users_type=instance,national_ID="",address="",staff_ID="",gender="",profile_pic="")
        if instance.user_type == 3:
            Staffs.objects.create(users_type=instance,national_ID="",address="",staff_ID="",gender="",profile_pic="")
        if instance.user_type == 4:
            Students.objects.create(users_type=instance,
                                    subject_id="",
                                    session_year_id="",
                                    student_class="",
                                    address="",
                                    student_id="",
                                    profile_pic="",
                                    gender="")
     
 
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()








