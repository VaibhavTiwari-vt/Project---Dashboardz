from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.core.mail import EmailMessage
from django.contrib import messages
from validate_email import validate_email
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

class LoginView(View):
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        context={
            'values':request.POST
        }
        if username and password:
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    messages.success(request,'Welcome, '+username+' You are now logged in')
                    return redirect('login')
                messages.error(request,"Account is not active, check your email",context)
                return render(request,'authentication/login.html')
            messages.error(request,"Invalid username or password")
            return render(request,'authentication/login.html',context)
        messages.error(request,"Please fill all the fields")
        return render(request,'authentication/login.html',context)

    def get(self,request):
        return render(request,'authentication/login.html')
    
class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    def post(self,request):
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        context={
            'fieldValues':request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(password=password).exists():
                if len(password)<8:
                    messages.error(request,"Password should be atleast 8 characters long")
                    return render(request,'authentication/register.html',context)
                user=User.objects.create_user(username=username,email=email)    #Account Creation
                user.set_password(password)                                     #Setting Password
                user.is_active=True
                user.save()                                                     #Saving User Detail
                email_subject='Activate your account'
                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                domain=get_current_site(request).domain
                link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
                activate_url='http://'+domain+link
                email_body='Hi '+user.username+' Use link to activate your account\n\n'+activate_url
                email = EmailMessage( email_subject,email_body,"noreply@semycolon.com",[email])
                EmailThread(email).start()
                messages.success(request,"Account Created Successfully")        #Success Message
                return redirect('login')
        return render(request,'authentication/register.html')

class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)
        except(TypeError,ValueError,OverflowError,User.DoesNotExist):
            user=None
        if user is not None and token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Account activated Successfully")        #Success Message
            return redirect('login')
        elif not token_generator.check_token(user,token):
            return redirect('login')
        elif user.is_active:
            return redirect('login')
        else:
            messages.error(request,'Account link invalid')
            return redirect('login')

class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send(fail_silently=False)

class UsernameValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        username=data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should only contain alphanumeric characters.'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Username already exists.'},status=400)
        return JsonResponse({'username_valid':True})
class EmailValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        email=data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Invalid Email.'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Email already exists.'},status=400)
        return JsonResponse({'email_valid':True})
    
class RequestPasswordResetEmail(View):
    def get(self,request):
        return render(request,'authentication/reset-password.html')
    def post(self,request):
        email=request.POST['email']
        context={"values":request.POST}
        if not validate_email(email):
            messages.error(request,"Please enter registered email address.",context)
            return render(request,'authentication/reset-password.html')
        email_subject='Password Reset'
        user=User.objects.filter(email=email)
        if user.exists():
            uidb64=urlsafe_base64_encode(force_bytes(user[0].pk))
            domain=get_current_site(request).domain
            link=reverse('reset-password-link',kwargs={'uidb64':uidb64,'token':PasswordResetTokenGenerator().make_token(user[0])})
            reset_url='http://'+domain+link
            email_body='Hi '+user[0].username+' Click the below link to reset your password.\n\n'+reset_url
            email = EmailMessage( email_subject,email_body,"noreply@semycolon.com",[email])
            EmailThread(email).start()
        messages.success(request,"Check you registered email address.")
        return render(request,'authentication/reset-password.html')

class CompletePasswordReset(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.error(request,"Invalid link")
                return redirect('login')
        except Exception as e:
            pass
        return render(request,'authentication/set-new-password.html',context)
    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['password']
        confirmPassword=request.POST['confirmPassword']
        if password!=confirmPassword:
            messages.error(request,"Passwords do not match.")
            return render(request,'authentication/set-new-password.html',context)
        if len(password)<6:
            messages.error(request,"Password should be at least 6 characters long.")
            return render(request,'authentication/set-new-password.html',context)
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)
            user.set_password(password) #This method is used to hash the password before saving it into the database. It ensures that the password is not stored in plain text but rather as a securely hashed value.
            user.save() #For other fields in the model (such as email, username, first_name, or any custom field you've defined), you simply assign the value directly without any special methods.
            messages.success(request,"Password changed successfully")
            return redirect('login')
        except Exception as e:
            messages.info(request,"Something is wrong.")
            return render(request,'authentication/set-new-password.html',context)
        
class LogoutView(View):
    def post(self,request):
        logout(request)
        messages.success(request,"You have been logged out")
        return redirect('login')