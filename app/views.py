from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, mail_admins
from .forms import ContactUsForm, UserSetting, ContactAdminForm ,DonationsForm
from django.http import HttpResponse
from portfolio.models import Project
from blog.models import Blog
from app import models
from django.contrib import messages
from accounts.form import RegisterUserForm
from .models import SmmaryDataBank
from .models import Scholarship 
from app import models
from accounts import models as m1
from blog import urls
from django.core.exceptions import ValidationError
from blog.forms import BlogForm


def Scholarship(request):
    # scholarship = Scholarship.objects.filter().order_by('title')
    return render(request, 'Scholarship.html', {'scholardata': models.Scholarship.objects.all()})


@login_required
def home(request):
    """
    Home page func
    Get request and return home page
    """
    return render(request, 'home.html', status=200)


@login_required
def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        proj = Project.objects.filter(title__contains=searched)
        blog = Blog.objects.filter(title__contains=searched)
        user = CustomUser.objects.filter(username__contains=searched)
        return render(request, 'search.html', {'searched': searched, 'projects': proj, 'blogs': blog, 'users': user}, status=200)
    else:
        return render(request, 'search.html', status=200)


@login_required
def personalArea(request):
    return render(request, 'personalArea.html', status=200)


@login_required
def logoutuser(request):  # p
    if request.method == 'POST':  # method post!!!
        logout(request)
        return redirect('home')  # return home page after logout


@login_required
def userSettings(request):
    user = get_object_or_404(CustomUser, pk=request.user.id)
    if request.method == 'GET':
        form = UserSetting(instance=user)
        return render(request, 'userSettings.html', {'user':user, 'form':form})
    else:
        try:
            form = UserSetting(request.POST, request.FILES, instance=user)
            form.save()
            if validator(request.POST['password1'], request.POST['password2']):
                user.set_password(request.POST['password1'])
                user.save()
            return redirect('personalArea')
        except ValueError:
            return render(request, 'userSettings.html', {'user':user, 'form':form, 'error': 'Bad info'})



def validator(val1, val2):
    if val1 != '' and val1 == val2:
        return True
    return False


def signupuser(request):
    """
    Sign up func

    """

    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form': RegisterUserForm()})  # User creation form
    else:
        if request.POST['password1'] == request.POST['password2']:  # if first and second password equal create new user
            try:
                user = CustomUser.objects.create_user(request.POST['username'], password=request.POST['password1'],
                                                      first_name=request.POST['first_name'],
                                                      last_name=request.POST['last_name'],
                                                      college=request.POST['college'],
                                                      date_of_birth=request.POST['date_of_birth'],
                                                      gender=request.POST['gender'], email=request.POST['email'],
                                                      major=request.POST['major'])  # create user
                user.save()  # save user
                login(request, user)
                messages.success(request, ("Registration Successful!"))
                return redirect('home')  # return current page
            except ValidationError as e:
                if 'email field must be unique' in e.error_message:
                    return render(request, 'signupuser.html', {'form': RegisterUserForm(),
                                                               'error': 'That email is already in use. Please try again.'})
                else:
                    return render(request, 'signupuser.html', {'form': RegisterUserForm(), 'error': e.error_message})
            except IntegrityError:
                return render(request, 'signupuser.html', {'form': RegisterUserForm(),
                                                           'error': 'That username has already been taken. Please try again.'})
                # if user create login that exist send error massege
        else:
            return render(request, 'signupuser.html', {'form': RegisterUserForm(), 'error': 'Passwords did not match'})



def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})  # Authentication Form
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('home')  # return current page


def contactus(request):
    """
    Contact US func
    Get request and return contactus page
    """
    if request.method == 'GET':
        return render(request, 'contactus.html')
    else:
        form = ContactUsForm(request.POST)
        message = 'Message was sent successfully'
        hasError = False
        if form.is_valid():
            form.save()
            form = ContactUsForm()
            form.fields['name'] = ''
            form.fields['email'] = ''
            form.fields['subject'] = ''
            form.fields['message'] = ''
            recipients = ['serj.moskovec@gmail.com']
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            from_email = request.POST.get('email', '')
            send_mail(subject, message, from_email, recipients)
        else:
            hasError = True
            message = 'Please make sure all fields are valid'

    return render(request, 'contactus.html', {'form': form, 'message': message, 'hasError': hasError})


def contactadmin(request):
    """
    Contact US func
    Get request and return contactus page
    """
    if request.method == 'GET':
        return render(request, 'contactadmin.html')
    else:
        form = ContactAdminForm(request.POST)
        message = 'Message was sent successfully'
        hasError = False
        if form.is_valid():
            form = ContactAdminForm(request.POST)
            form.save()
            

        else:
            hasError = True
            message = 'Please make sure all fields are valid'

    return render(request, 'contactadmin.html', {'form': form, 'message': message, 'hasError': hasError})

def donations(request): 
    """
    Donations func
    Get request and return donations page
    """
    if request.method == 'GET':
        return render(request, 'donations.html')
    else:
        form = DonationsForm(request.POST)
        message = 'Your donation was sent successfully!! Thanks!!'
        hasError = False
        if form.is_valid():
            form.save()
            form = DonationsForm()
            form.fields['amount'] = ''
            form.fields['scholarship'] = ''
            form.fields['reason'] = ''
            form.fields['email'] = ''
            form.fields['message'] = ''
        else:
            hasError = True
            message = 'Please make sure all fields are valid'
            
    return render(request, 'donations.html', {'form': form, 'message': message, 'hasError': hasError })


def SmmaryDataBank(request):
    if request.method == "GET":
        name = request.GET.get('NameOfFile')
        file = request.GET.get('AddFile')
        data = models.SmmaryDataBank(name=name, file=file)
        data.save()
        return render(request, 'SmmaryDataBank.html')
    return render(request, 'SmmaryDataBank.html', {'data': models.SmmaryDataBank.objects.all()})


@login_required
def all_blogs(request):
    blogs = Blog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'all_blogs.html', {'blogs': blogs})


@login_required
def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    return render(request, 'detail.html', {'blog': blog})


@login_required
def createBlog(request):
    if request.method == 'GET':
        return render(request, 'createPost.html')
    else:
        try:
            form = BlogForm(request.POST)  # edit form
            newblog = form.save(commit=False)  # save all input data in database
            newblog.user = request.user
            newblog.save()  # save data
            return redirect('all_blogs')
        except ValueError:
            return render(request, 'createPost.html', {'form': BlogForm(), 'error': 'Bad data passed in. Try again'})


@login_required
def editBlog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'GET':
        form = BlogForm(instance=blog)
        return render(request, 'editBlog.html', {'blog': blog, 'form': form})
    else:
        try:
            form = BlogForm(request.POST, instance=blog)
            form.save(blog)
            return redirect('detail', blog_id)
        except ValueError:
            return render(request, 'editBlog.html', {'blog': blog, 'form': form, 'error': 'Bad info'})


@login_required
def deleteBlog(request, blog_id):  # delete can do only user who create todo
    blog = get_object_or_404(Blog, pk=blog_id,
                             user=request.user)  # find todo in database(import get_object_or_404), (user=request.user) check if todo belongs to user
    if request.method == 'POST':  # Post becouse we upload data to database
        Blog.delete(blog)  # delete blog
        return redirect('all_blogs')  # return page with current todos
    # ?????????????????????????????????????????????????
    # /////////////////////////////////////////////////
    # ?????????????????????????????????????????????????
    # /////////////////////////////////////////////////


def add_ScholarShip(request,id):
    user = m1.CustomUser.objects.get(id=request.user.id)
    scholar = models.Scholarship.objects.get(id=id)
    user.Scholarship.add(scholar)
    context = {
    'items': models.Scholarship.objects.all(),
    'scholardata': 'Items'}


    print(Scholarship)

    return render(request,'SmmaryDataBank.html',context=context)
    
