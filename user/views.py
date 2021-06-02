from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string

from user.forms import SignUpForm
from user.tokens import account_activation_token
from .models import *

import datetime

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

def index(request):
    if not request.user.is_authenticated:
        is_guest = 0
    else:
        is_guest = 1
    now = datetime.datetime.now()
    months = ["January", "February", "March", "April",
              "May", "June", "July", "August", "September",
              "October", "November", "December"]
    return render(request,"user/index.html",{
        "now": now,
        "month": months[now.month-1],
        "users": Profile.objects.all(),
        "posts": Post.objects.all(),
        "is_guest": is_guest
    })

def newpost(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user:index"))
    else:
        return render(request, "user/newpost.html")

def returnuserpage(request,name,form):
    if form == None:
        return render(request, "user/userpage.html", {
                "name": name,
                "tasks": request.session["tasks"],
                "form": NewTaskForm()
                 })
    else:
       return render(request, "user/userpage.html", {
            "name": name,
            "tasks": request.session["tasks"],
            "form": form
             }) 

def userpage(request, name):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return returnuserpage(request,name,None)
        else:
          return returnuserpage(request,name,form)   
    else:
        return returnuserpage(request,name,None)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("user:index"))
        else:
            return render(request, "user/login.html", {
                "message": "Invalid credentials."
            })
    return render(request, "user/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user:index"))

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Dender Account'
            message = render_to_string('user/accountactivation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return HttpResponseRedirect(reverse("user:account_activation_sent"))
    else:
        form = SignUpForm()
    return render(request, "user/signup.html", {'form': form})

def account_activation_sent(request):
    return render(request, "user/activationsent.html")

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activationinvalid.html')

