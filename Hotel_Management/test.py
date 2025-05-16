d1={"r_n":[1,2,1],
    "adult":[2,1,0],
    "child":[0,0,0]}

# for x,j in enumerate(d1.items()):
#     print(j[1])


a={'booking_dates': {'from_date': '2025-02-01', 'to_date': '2025-02-02'}, 'personal_details': {'country': 'India', 'email': 'kinshukjanga@gmail.com', 'first_name': 'Kinshuk Jangra', 'phone': '9910210998', 'title': 'Mr.'}, 'rooms': [{'adults': 2, 'children': 0, 'name': 'Deluxe', 'room': 1}]}
b={'booking_dates': {'from_date': '2025-02-01', 'to_date': '2025-02-02'}, 'personal_details': {'country': 'India', 'email': 'kinshukjanga@gmail.com', 'first_name': 'Kinshuk Jangra', 'phone': '9910210998', 'title': 'Mr.'}, 'rooms': [{'adults': 2, 'children': 0, 'name': 'Deluxe', 'room': 1}, {'adults': 2, 'children': 0, 'name': 'Deluxe', 'room': 2}, {'adults': 2, 'children': 0, 'name': 'Deluxe', 'room': 3}, {'adults': 2, 'children': 0, 'name': 'Deluxe', 'room': 4}]}


a={'rooms': [{'adults': 2, 'children': 0, 'name': 'Deluxe', 'room': 1},
              {'adults': 2, 'children': 0, 'name': 'Deluxe', 'room': 2}, 
              {'adults': 2, 'children': 0, 'name': 'Deluxe', 'room': 3}, 
              {'adults': 2, 'children': 0, 'name': 'Deluxe', 'room': 4}]}
Invalid block tag on line 74: 'endblock', expected 'empty' or 'endfor'. Did you forget to register or load this tag?

Reverse for 'otp-Verify' not found. 'otp-Verify' is not a valid view function or pattern name.



from django.shortcuts import render ,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate ,login ,logout
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .forms import login_form ,RegisterForm,Otp_check
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

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
            
            # Check if input is an email or username
            user = None
            if User.objects.filter(email=email_or_username).first():
                user = User.objects.get(email=email_or_username).first()
                user = authenticate(request, username=user.username, password=password)  # Use username for auth
            else:
                user = authenticate(request, username=email_or_username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('/')  
            else:
                messages.info(request, "Invalid credentials. Please try again.")
                return redirect('login')

    return render(request, "login.html", {"form": form})


def logout_user(request):
    messages.success(request, "Loged out.")
    logout(request)
    return redirect("/")




def user_dashboard(request):
    if request.user.is_authenticated:
        user=request.user
        return render(request,"user.html",{"user":user})
    else:
        messages.info(request,"You are not loged in")
        return redirect('login')



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

def otp_verification(request):
    if request.user.is_authenticated:
        messages.info(request,"You are already loged in")
        return redirect('home')
    
    if not request.session.get("otp"):
        messages.info(request,"You can't access this page")
        return redirect('login')
    form=Otp_check()

    if request.method == "POST":
        form = Otp_check(request.POST)
        if form.is_valid():

            entered_otp =form.cleaned_data['otp']
            stored_otp = request.session.get("otp")
            email = request.session.get("email")
        if entered_otp and stored_otp and int(entered_otp) == stored_otp:
            user = User.objects.create_user(username=email, email=email, password="default123")  # Create user
            user.is_active = True  # Activate after OTP verification
            user.save()

            del request.session["otp"]  # Remove OTP from session
            del request.session["email"]

            messages.success(request, "Account verified! You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Invalid OTP. Try again.")

    return render(request, "otp.html",{"form":form})

def signin_user(request):
    if request.user.is_authenticated:
        messages.error(request, "Already logged in")
        return redirect("/")  

    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            otp = random.randint(100000, 999999)  # Generate OTP
            request.session["otp"] = otp  # Store OTP in session
            request.session["email"] = email  # Store email
            a=send_mail(email, otp)  # Send OTP via email
            if not a:
                messages.info(request, "email not send")
            messages.success(request, "OTP sent to your email. Verify to continue.")
            return redirect("otp_verify")  # Redirect to OTP verification page

    return render(request, "sign.html", {"form": form})
















from django.contrib.auth import authenticate ,login ,logout
from django.contrib.auth.models import User
from django.shortcuts import render ,redirect,HttpResponse
from home.models import R_D , Rooms,Comment , Contact , temp,User_Booked_Room_Details
from django.contrib import messages 
import time
import os
from .forms import comments_form ,Contact_form , booking_details_form
from datetime import date, timedelta
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




def home(request):
    rooms=R_D.objects.all()
    for room in rooms:
            room.image= f"static/image/{room.room_type}/1.png"
    return render(request,'home.html',{"rooms":rooms})


def rooms(request):
    
    rooms=R_D.objects.all()
    for room in rooms:
            room.image= f"static/image/{room.room_type}/1.png"
    return render(request,"room.html",{"rooms":rooms})


def gallery(request):
     return render(request,"gallery.html",{})
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from .forms import Contact_form  # Ensure you have a Django form class

def contact(request):
    form = Contact_form()  # Ensure form is always available

    if request.method == "POST":
        if request.user.is_authenticated:
            subject = request.POST.get("subject")
            message = request.POST.get("message")

            if not message:
                messages.info(request, "Message can't be empty")
                return redirect("contact")
            new = Contact(
                username=request.user.username,
                email=request.user.email,
                subject=subject,
                message=message
            )
            new.save()

            messages.success(request, "Thank you for your message! We will contact you as soon as possible.")
            return redirect("contact")

        else:
            form = Contact_form(request.POST)  
            if form.is_valid(): 
                username =form.cleaned_data['username']
                email =form.cleaned_data['email']
                subject =form.cleaned_data['subject']
                message =form.cleaned_data['message']
                new = Contact(
                username=username,
                email=email,
                subject=subject,
                message=message
            )
                new.save()  
                
                messages.success(request, "Thank you for your message! We will contact you as soon as possible.")
                return redirect("contact")

    # Ensure form is always available, even on GET requests
    context = {
        "form": form,
    }

    if request.user.is_authenticated:
        context["details"] = request.user

    return render(request, "contact.html", context)


def details_room(request,id):
    if not R_D.objects.filter(id=id):
        return redirect("/404")
    room = R_D.objects.filter(id=id).first()
    image ={}
    for x in range(1,3):
        a=f"static/image/{room.room_type}/{x}.png"
        if os.path.exists(a):   
            image[f"image{x}"] = a

    avilable_rooms= Rooms.objects.filter(room_type=room.room_type,room_availability=True ).all()
    avi=0
    for x in avilable_rooms:
        avi+=1  
    
    comments = Comment.objects.filter(room_type=room.room_type)
    form=comments_form()
    if request.method =="POST":
        form = comments_form(request.POST)
        if form.is_valid():
            message=form.cleaned_data["message"]
            if request.user.is_authenticated:
                new_com = Comment(
                room_type=room,  # Pass room_type as a string
                username=request.user,    # Use the currently logged-in user
                message=message)
                new_com.save()
                messages.info(request,"Message summited successfully")
                return redirect(request.path)
            else:
                messages.info(request,"please login first")
                return redirect("register/login")
    else:
        form= comments_form()

         
    return render(request,"det_room.html",{"room":room,"image":image,"available":avi,"comments":comments,"form":form})

def page_not_found(request):
    return render(request,"404.html")

def booking(req, id=0):
    form = booking_details_form()  
    room = R_D.objects.filter(id=id).first()
    if room is None:
        room = R_D.objects.first() 
    avi = {"available_rooms": Rooms.objects.filter(room_availability=True).count()}

    initial_data = {}
    if req.user.is_authenticated:
        initial_data = {
            "name": req.user,
            "email": req.user.email,
        }
        

    if req.method == "POST":
        form = booking_details_form(req.POST) 
        if form.is_valid():
            global data
            data = {
                "from_date": form.cleaned_data.get("from_date"),
                "to_date": form.cleaned_data.get("TO_date"),
                "title": form.cleaned_data["title"],
                "name": req.user.username if req.user.is_authenticated else form.cleaned_data["name"],
                "email": req.user.email if req.user.is_authenticated else form.cleaned_data["email"],
                "phone": form.cleaned_data["phone"],
                "country": form.cleaned_data["country"],
                "room": int(req.POST.get('room_count')),
                "room_name":room.room_type,
            }
            sorted_data = User_Booked_Room_Details.objects.filter(datetime.today()<from_date>)

            try:
                room_count = int(data["room"])
                if room_count > avi["available_rooms"]:
                    messages.info(req, f"Can't add more rooms than {avi['available_rooms']}")
                    return redirect(f"/booking-{id}")
            except (TypeError, ValueError):
                messages.info(req, "Invalid room count.")
                return redirect(f"/booking-{id}")


            #checking dates
            from_date = data["from_date"]
            to_date = data["to_date"]
            
            # Make sure from_date and to_date are valid before comparing
            if from_date and to_date:
                if to_date < from_date or to_date < date.today() or from_date < date.today():
                    messages.info(req, "You have entered wrong dates")
                    return redirect('/booking-1')
            else:
                # If dates are not provided, show an error
                messages.info(req, "Please enter valid dates.")
                return redirect(f'/booking-{id}')
            

            global adult, child

            #getting adults and child 
            adult={"room_1":req.POST.get('ra-1')}
            child={"room_1":req.POST.get('rc-1')}
            if 1<int(data["room"])<=avi["available_rooms"]:
                for x in range(2, int(data["room"]) + 1):
                    adult[f"room_{x}"]=req.POST.get(f"adult_c-{x}")  
                    child[f"room_{x}"]=req.POST.get(f"child_c-{x}")

            #check data of adults and childs
            for x in adult:
                if int(adult.get(x))>room.space_for_adult:
                    messages.info(req,f'can only add {room.space_for_adult}/pr room')
                    return redirect(f"/booking-{id}")

            for x in child:
                if int(child.get(x))>room.space_for_child:
                    messages.info(req,f'can only add {room.space_for_child}/pr room')
                    return redirect(f"/booking-{id}")
            return redirect(f"/booking_details-{room.id}")  # Redirect after successful submission
        
        else:
            messages.info(req, "Please fill all the details correctly.")
    else:
        form = booking_details_form(initial=initial_data)  # Pre-fill form with initial values
    
    # Make name and email fields readonly
    if req.user.is_authenticated:
        form.fields["name"].widget.attrs["readonly"] = True
        form.fields["email"].widget.attrs["readonly"] = True

    return render(req, "booking.html", {"room": room, "data": avi, "form": form})   


def booking_details(request,id=0):
    global data, child,adult
    try:
        room = R_D.objects.filter(id=id).first()
        if room is None:
            room = R_D.objects.first() 
        a=[]
        global t_a ,t_c
        t_a=0
        t_c=0
        for x in range(1,data["room"]+1):
            tmp={"adults":adult[f"room_{x}"],"children":child[f"room_{x}"],"name":room.room_type,"room":x}
            t_a+=int(adult[f"room_{x}"])
            t_c+=int(child[f"room_{x}"])
            a.append(tmp)

        days = (data["to_date"] - data["from_date"]).days
        total=days*room.price*data["room"]
        data['total']=total
        if data and child and adult:
            return render(request,'pay.html',{"room":room,"data":data,"room_data":a,"total":total})
        else:
            messages.info(request,"you can't access this page")
            return redirect('/')
    except Exception as e:
        messages.info(request,f"you can't access this page:{e}")
        return redirect('/')




def Booked(req):
    new=User_Booked_Room_Details(username=req.user.username if req.user.is_authenticated else data["name"],
                                 email=req.user.email if req.user.is_authenticated else data["email"],
                                 phone=data["phone"],
                                 room_type=data['room_name'],
                                 number_of_rooms =data["room"],
                                 adults=t_a,
                                 child=t_c,
                                check_in =data["from_date"],
                                check_out=data['to_date'],
                                total_amount=data["total"]
                                 )
    new.save()
    return HttpResponse("data submited successfully")




import threading
import time
from datetime import datetime, timedelta

task_scheduled = False 
def background_task():
    rooms = Rooms.objects.filter(room_availability=False).all()

    for x in rooms:
        if x.to_date + timedelta(days=1) >= datetime.today().date():
            x.to_date = None  
            x.from_date = None 
            x.room_availability = True
            x.save()

def schedule_task():
    global task_scheduled
    if task_scheduled:
        print("Task already scheduled, skipping...")
        return

    task_scheduled = True 
    now = datetime.now()
    next_run = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    sleep_time = (next_run - now).total_seconds()

    print(f"Task scheduled to run at {next_run}")
    time.sleep(sleep_time)  
    background_task()



if not task_scheduled:
    task_thread = threading.Thread(target=schedule_task, daemon=True)
    task_thread.start()




# have to properly setup the booked route 