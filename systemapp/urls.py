from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from . import views
from .import AdminViews, StaffViews, StudentViews

app_name = 'school'
urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('test/', views.test, name="test"),

    path('contact', views.contact, name="contact"),
    path('login', views.loginUser, name="login"),
    path('logout_user', views.logoutUser, name="logout_user"),
    path('registration', views.registration, name="registration"),
    path('doLogin', views.loginpage, name="doLogin"),
    path('doRegistration', views.doRegistration, name="doRegistration"),
    path('newtrRegistration', AdminViews.teacher_registration, name="newtrRegistration"),
    path('inbox', views.inbox, name="inbox"),

     
    # URLS for Student
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_view_attendance/', StudentViews.student_view_attendance, name="student_view_attendance"),
    #path('student_view_attendance_post/', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    #path('student_apply_leave/', StudentViews.student_apply_leave, name="student_apply_leave"),
    #path('student_apply_leave_save/', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback/', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save/', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    # path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),
    path('student_view_result/', StudentViews.student_view_result, name="student_view_result"),
    path('student_report/', StudentViews.student_report, name="student_report"),
 
 
     # URLS for Staff
    path('staff_home/', StaffViews.staff_home, name="staff_home"),
    path('staff_take_attendance/', StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path('get_students/', StaffViews.get_students, name="get_students"),
    path('class_students/<class_id>/', StaffViews.staff_class_students, name="staff_class_students"),
    #path('save_attendance_data/', StaffViews.save_attendance_data, name="save_attendance_data"),
    #path('staff_update_attendance/', StaffViews.staff_update_attendance, name="staff_update_attendance"),
    #path('get_attendance_dates/', StaffViews.get_attendance_dates, name="get_attendance_dates"),
    #path('get_attendance_student/', StaffViews.get_attendance_student, name="get_attendance_student"),
    #path('update_attendance_data/', StaffViews.update_attendance_data, name="update_attendance_data"),
    path('staff_apply_leave/', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_feedback/', StaffViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save/', StaffViews.staff_feedback_save, name="staff_feedback_save"),
    path('staff_profile/', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_update/', StaffViews.staff_profile_update, name="staff_profile_update"),
    path('staff_add_result/', StaffViews.staff_add_result, name="staff_add_result"),
    path('staff_add_marks/<student_id>/', StaffViews.staff_add_marks, name="staff_add_marks"),
    path('staff_edit_marks/<student_id>/', StaffViews.staff_edit_marks, name="staff_edit_marks"),

    path('staff_students/<subject_id>', StaffViews.staff_students, name="staff_students"),
    path('staff_students_all/', StaffViews.staff_students_all, name="staff_students_all"),
  

    # URL for Admin
    path('admin_home/', AdminViews.admin_home, name="admin_home"),
    path('add_staff/', AdminViews.add_staff, name="add_staff"),
    path('manage_staff/', AdminViews.manage_staff, name="manage_staff"),
    path('manage_teachers/', AdminViews.manage_teacher, name="manage_teachers"),
    path('teacher_details/<teacher_id>', AdminViews.teacher_view, name="teacher_details"),
    path('edit_staff/<staff_id>/', AdminViews.edit_staff, name="edit_staff"),
    # path('edit_staff_save/', AdminViews.edit_staff_save, name="edit_staff_save"),
    path('delete_staff/<staff_id>/', AdminViews.delete_staff, name="delete_staff"),
    path('add_class/', AdminViews.add_class, name="add_class"),
    # path('add_class_save/', AdminViews.add_class_save, name="add_class_save"),
    path('manage_class/', AdminViews.manage_class, name="manage_classes"),
    path('previous_class/', AdminViews.previous_class, name="previous_classes"),
    path('edit_class/<class_id>/', AdminViews.edit_class, name="edit_class"),
    # path('edit_class_save/', AdminViews.edit_class_save, name="edit_class_save"),
    path('delete_class/<class_id>/', AdminViews.delete_class, name="delete_class"),
    path('manage_session/', AdminViews.manage_session, name="manage_session"),
    path('add_session/', AdminViews.add_session, name="add_session"),
    # path('add_session_save/', AdminViews.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', AdminViews.edit_session, name="edit_session"),
    # path('edit_session_save/', AdminViews.edit_session_save, name="edit_session_save"),
    path('delete_session/<session_id>/', AdminViews.delete_session, name="delete_session"),
    path('add_student/', AdminViews.add_student, name="add_student"),
    path('student_details/<student_id>', AdminViews.student_view, name="student_details"),
    # path('add_student_save/', AdminViews.add_student, name="add_student_save"), 
    path('edit_student/<student_id>', AdminViews.edit_student, name="edit_student"),
    # path('edit_student_save/', AdminViews.edit_student_save, name="edit_student_save"),
    path('manage_student/', AdminViews.manage_student, name="manage_student"),
    path('delete_student/<student_id>/', AdminViews.delete_student, name="delete_student"),
    path('add_subject/', AdminViews.add_subject, name="add_subject"),
    # path('add_subject_save/', AdminViews.add_subject_save, name="add_subject_save"),
    path('manage_subject/', AdminViews.manage_subject, name="manage_subject"),
    path('edit_subject/<subject_id>/', AdminViews.edit_subject, name="edit_subject"),
    # path('edit_subject_save/', AdminViews.edit_subject_save, name="edit_subject_save"),
    path('delete_subject/<subject_id>/', AdminViews.delete_subject, name="delete_subject"),
    path('check_email_exist/', AdminViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', AdminViews.check_username_exist, name="check_username_exist"),
    path('student_feedback_message/', AdminViews.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_reply/', AdminViews.student_feedback_message_reply, name="student_feedback_message_reply"),
    path('staff_feedback_message/', AdminViews.staff_feedback_message, name="staff_feedback_message"),
    path('staff_feedback_message_reply/', AdminViews.staff_feedback_message_reply, name="staff_feedback_message_reply"),
    #path('student_leave_view/', AdminViews.student_leave_view, name="student_leave_view"),
    #path('student_leave_approve/<leave_id>/', AdminViews.student_leave_approve, name="student_leave_approve"),
    #path('student_leave_reject/<leave_id>/', AdminViews.student_leave_reject, name="student_leave_reject"),
    path('staff_leave_view/', AdminViews.staff_leave_view, name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/', AdminViews.staff_leave_approve, name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/', AdminViews.staff_leave_reject, name="staff_leave_reject"),
    #path('admin_view_attendance/', AdminViews.admin_view_attendance, name="admin_view_attendance"),
    #path('admin_get_attendance_dates/', AdminViews.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    #path('admin_get_attendance_student/', AdminViews.admin_get_attendance_student, name="admin_get_attendance_student"),
    path('admin_profile/', AdminViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', AdminViews.admin_profile_update, name="admin_profile_update"),
         

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)