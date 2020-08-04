from django.shortcuts import render
from pass_app.forms import UserForm,UserProfileInfoForm
from django.http import HttpResponse,HttpResponseRedirect

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    return render(request,'pass_app/index.html')

def register(request):
    registered=False
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #grab the user_form and save to the database ,then hashing the password and lastly save the password change to the user
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)#dont save to the database to avoid collision
            profile.user=user#the one-to-one relation set 

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm
    return render(request,'pass_app/registration.html',{'registered':registered,'user_form':user_form,'profile_form':profile_form})

def user_login(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse('ACCOUNT IS NOT ACTIVE')
            
        else:
            print("Someone tries to login to the page and failed")
            print(f"Username:{username} ans Password:{password}")
            return HttpResponse("Invalid login details")
    else:
        return render(request,'pass_app/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def special(request):
    return HttpResponse("you are login .. nice!!")