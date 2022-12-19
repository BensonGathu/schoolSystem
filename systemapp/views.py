from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import  SessionYearModel, StudentResult, Admin, Staffs, FeedBackStaffs, NotificationStaffs, Classes, Subjects, Students, StudentResult, FeedBackStudent, NotificationStudent, Timetable, Exams
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib import messages
# Create your views here.

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync



def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",

        {
            'type':"send_notification",
            'message':"test notification"
        }
    )

    return HttpResponse("Done")




def home(request):
    return render(request, 'home.html')


def contact(request):
    return render(request, 'contact.html')


def loginUser(request):
    return render(request, 'auth/login_page.html')


def loginpage(request):
    pass
    if request.method == 'POST':
        # email_id = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
		
      
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in as' + ' ' + username)
           
            if user.is_student:
                return redirect('school:student_home')

            elif user.is_admin and user.is_staff:
                return redirect("school:admin_home")
                
            elif user.is_staff:
                return redirect('school:staff_home')
           
                
            elif user.is_teacher:
                return redirect('school:staff_home')
           
           
        else:
            messages.error(request, 'Invalid Username and/or Password')

    context = {}
    return render(request, 'auth/login_page.html')


	

def logoutUser(request):
    current_user = request.user
    logout(request)
    messages.info(
        request, 'You have logged out.')  
    # if current_user.is_admin:
    return redirect('school:doLogin')
    



def registration(request):
    form = CreateUserForm()
    context = {
            "form": form
    }
    return render(request, 'auth/registration.html', context)


def doRegistration(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            
            first_name = form.cleaned_data['firstname']
            last_name = form.cleaned_data.get('lastname')
            email_id = form.cleaned_data.get('email')
            
            # password = form.cleaned_data.get('password1')
            # confirm_password = form.cleaned_data.get('password2')


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


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


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


def inbox(request):
    context = {

    }
    return render(request, 'inbox.html', context)
