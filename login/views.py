from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from quoteApp.models import Quote
import re

# Create your views here.
def index(request):
    request.session.clear()
    return render(request, 'index.html')

def register(request): 
    if request.method == "POST": 
        errors = User.objects.validator(request.POST) 
        if len(errors) != 0: 
            for key, value in errors.items(): 
                messages.error(request, value) 
            return redirect('/') 
        else: 
            new_user = User.objects.register(request.POST)
            new_user.fname = new_user.fname.title()
            request.session['user_id'] = new_user.id
            request.session['name'] = new_user.fname
            # UNCOMMENT BELOW and CHANGE FOR EXAM
            return redirect('/quotes') 
    return redirect('/')

def login(request): 
    if request.method == "GET":
        return render(request, "index.html")
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, "Invalid Email or Password")
        return redirect('/')

    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id 
    request.session['name'] = user.fname
    # UNCOMMENT BELOW and CHANGE FOR EXAM
    return redirect('/quotes') 
    # return redirect('/')

def userQuotes(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=id)
    user_quotes = Quote.objects.filter(poster=user)
    context = {
        'user': user,
        'user_quotes': user_quotes,
    }
    return render(request, "userQuotes.html", context)

def myAccount(request, id):
    if request.session['user_id'] is not id:
        messages.error(request, "You can't access this account")
        return redirect(f"/myaccount/{id}")
        
    user = User.objects.get(id=id)
    if request.method == "GET":
        context = {
            'user': user,
        }
        return render(request, "editAccount.html", context)

    if request.method == "POST":
        errors = User.objects.emailValidator(request.POST)
        if len(errors) != 0: 
            for key, value in errors.items(): 
                messages.error(request, value) 
            return redirect(f'/myaccount/{user.id}') 

        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.email = request.POST['email']
        user.save()
    return redirect('/quotes')


def logout(request): 
    request.session.flush() 
    return redirect('/')
