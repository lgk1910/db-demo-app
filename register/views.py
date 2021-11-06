from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            new_user.cart_set.create()
            messages.info(request, "Thanks for registering. You are now logged in.")
            return redirect("home")
        else:
            messages.error(request, "Check again the information")
            return render(request, "register/register.html", context={"form":form})
        
    else:
        form = RegisterForm()
    return render(request, "register/register.html", context={"form":form})