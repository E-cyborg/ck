from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import login_form, RegisterForm  # Ensure these are defined
from home.models import User_Booked_Room_Details

def loginUser(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('/')
    form = login_form()
    if request.method == "POST":
        form = login_form(request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data["email_or_username"]
            password = form.cleaned_data["password"]
            user = User.objects.filter(email=email_or_username).first()
            if user:
                user = authenticate(request, username=user.username, password=password)
            else:
                user = authenticate(request, username=email_or_username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('/')
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                return redirect('login')
    return render(request, "login.html", {"form": form})


def logout_user(request):
    messages.success(request, "Logged out.")
    logout(request)
    return redirect("/")

def signin_user(request):
    if request.user.is_authenticated:
        messages.error(request, "Already logged in.")
        return redirect("/")  

    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            if User.objects.filter(email=email).exists():  # Fixed syntax and logic
                messages.info(request, 'Email already exists. Please log in.')
                return redirect('/login')

            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')

    return render(request, "sign.html", {"form": form})


def user_dashboard(request):
    if request.user.is_authenticated:
        if User_Booked_Room_Details.objects.filter(username=request.user.username,email=request.user.email).all():
            tmp=User_Booked_Room_Details.objects.filter(username=request.user.username,email=request.user.email)
            return render(request, "user.html", {"user": request.user,"tmp":tmp})
        return render(request, "user.html", {"user": request.user})
    else:
        messages.info(request, "You are not logged in.")
        return redirect('login')



from django.contrib.auth.decorators import login_required
import random
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .forms import login_form ,RegisterForm,Otp_check
def send_mail(to, pin):
    try:
        subject = "Identity Verification"
        sender_email = settings.EMAIL_HOST_USER  # Use configured email
        html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; text-align: center;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; padding: 20px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);">
                    <h2 style="color: #333;">Verify Your Identity</h2>
                    <p style="font-size: 16px; color: #666;">
                        Dear User,<br><br>
                        Please use the following pin to verify your identity:
                    </p>
                    <h1 style="font-size: 24px; color: #333; margin-top: 0;">{pin}</h1>
                    <p style="font-size: 14px; color: #888;">
                        If you did not request this verification, please disregard this email.
                    </p>
                </div>
            </body>
            </html>
        """

        # Create email
        mail = EmailMultiAlternatives(subject, "", sender_email, [to])
        mail.attach_alternative(html_content, "text/html")  # Attach HTML version
        mail.send()
        return True
    except Exception as e:
        print("Email error:", e)  # Debugging
        return False

