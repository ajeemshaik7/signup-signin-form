from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def home(request):
    return render(request,"index.html")

def signup(request):

    if request.method == "POST":
        #alternate method to use (#username = request.post.get("username"))
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email was registered already!")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request, "Username does not exceed 10 characters")
           
        
        if (password!=password2):
            messages.error(request, "Passwords didn't match")

        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric!")
            return redirect('home')
            
        myuser=User.objects.create_user(username, email, password)

        myuser.first_name = firstname
        myuser.last_name = lastname
        #saving the user
        myuser.save()

        messages.success(request,"Your Account has been successfully created.")

        #sending email
        subject = "Hello,Welcome to Django Application login!"
        message = myuser.first_name+"Welcome to Django application,Please confirm your email to succesfull login!..."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return redirect('signin')


    return render(request,"signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "index.html",{'fname':fname})

        else:
            messages.error(request, "Bad Credentials")
            return redirect('home')
        

    return render(request,"signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out succesfully")
    return redirect('home')


















#ajeemshaik7