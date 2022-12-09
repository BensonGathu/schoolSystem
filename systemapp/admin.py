from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Admin, Staffs, Classes, Subjects, Students, LeaveReportStaff, FeedBackStudent, FeedBackStaffs, NotificationStudent, NotificationStaffs,SessionYearModel,StudentResult,User,leave_types

# Register your models here.
# class UserModel(UserAdmin):
# 	pass


# admin.site.register(CustomUser, UserModel)
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Staffs)
admin.site.register(Classes)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(StudentResult)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedBackStudent)
admin.site.register(FeedBackStaffs)
admin.site.register(NotificationStudent)
admin.site.register(NotificationStaffs)
admin.site.register(SessionYearModel)
admin.site.register(leave_types)
