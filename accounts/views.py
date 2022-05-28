from urllib import request
from django.shortcuts import redirect, render
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import LoginInfo
from django.contrib.auth.models import User

# Create your views here.


def login_req(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                print(request.user.id)
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, template_name="login.html", context={"login_form": form})


def signup(request):

    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                login_info = LoginInfo(user=user)
                login_info.save()
                return redirect("index")
            messages.error(
                request, "Unsuccessful registration. Invalid information.")
        form = NewUserForm()
        return render(request, template_name="signup.html", context={"register_form": form})


def logout_req(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")

def del_profile(request, id):    
        if request.user.id==id:
            u = User.objects.get(id = id)
            if u is not None:
                u.delete()
                messages.success(request, "The user is deleted")
            else:
                messages.error(request, "The user not found")
        else:
            messages.error(request,"can't delete someone else's profile!")
            
        return redirect("index")