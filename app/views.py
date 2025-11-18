from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user = User.objects.create(
                first_name = firstname,
                last_name = lastname,
                email = email,
                username = username,
                password = password,
                # confirm_password = confirm_password,
            )
            user.set_password(password)
            user.save()
            messages.success(request, "Registration successful! Please sign in.")
            return redirect('signin')

    return render(request,'registerform.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None:
            if user.is_authenticated:
                login(request,user)
                return redirect('home')

    return render(request,'signinform.html')


def home(request):
    return render(request,'homeform.html')



def signout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('signin')

@login_required
def update_password(request,id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        fm = PasswordChangeForm(user=user,data=request.POST)
        if fm.is_valid():
            fm.save()
            return  redirect('signout')
    context = {
        'form':PasswordChangeForm(user=user)
    }
    return render(request,'update_password.html',context)