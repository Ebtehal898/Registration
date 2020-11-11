from django.shortcuts import render, HttpResponse,redirect
from .models import User
from django.contrib import messages
import bcrypt

def index (request):
    if 'user_id' not in request.session:
        request.session['user_id'] = ""
    return render(request,'Login_Registration.html')


def register (request):
    if request.method == "POST":

        errors = User.objects.validate(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            birth_date = request.POST['birthday']
            new_user=User.objects.create(first_name=first_name, last_name=last_name, email=email,password=pw_hash, birthday=birth_date)
            request.session['user_id']=new_user.id
    return redirect ('/success')

def success (request):
    if request.session['user_id'] != "":
        context ={
            "user_name": User.objects.get(id=request.session['user_id']).first_name
        }
        return render(request,"Welcome.html",context)
    else:
        return redirect('/')    

def login (request):
    if request.method == "POST":
        errors = User.objects.validate_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.filter(email=request.POST['email']) 
            if user: # an empty list will return false
                logged_user = user[0] 
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    # if we get True after checking the password, we may put the user id in session
                    request.session['user_id'] = logged_user.id
                    # never render on a post, always redirect!
                    return redirect('/success')
                else:
                    messages.error(request, "Password is wrong!!")    
    return redirect("/")


def reset(request):
    request.session.clear()
    return redirect('/')    