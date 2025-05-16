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
import numpy as np



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


def details_room(request,id=0):
    room = R_D.objects.filter(id=id).first()
    if room is None:
        return redirect("details_room",0)  
    image ={}
    for x in range(1,3):
        a=f"static/image/{room.room_type}/{x}.png"
        if os.path.exists(a):   
            image[f"image{x}"] = a

    avilable_rooms = Rooms.objects.filter(room_type=room.room_type, room_availability=True).count()
    
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

         
    return render(request,"det_room.html",{"room":room,"image":image,"available":avilable_rooms,"comments":comments,"form":form})

def page_not_found(request):
    return render(request,"404.html")

def booking(req, id=0):
    # Get Room Details
    form = booking_details_form()  # Process form submission
    room = R_D.objects.filter(id=id).first()
    if room is None:
        return redirect("booking",1)  
    
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
            no_of_room = Rooms.objects.filter(room_type=room.room_type, room_availability=True).count()
            m_f = data["from_date"]
            m_t = data["to_date"]
            data_user = User_Booked_Room_Details.objects.filter(check_out__gte=m_f, check_in__lte=m_t)
            l = []

            for x in data_user:
                if not (x.check_out < m_f or x.check_in > m_t):
                    l.append(json.loads(x.room_allocated)) 
            l = np.array(l).ravel()
            l = sorted(set(map(int, l)))
            global exact_avilable_rooms
            exact_avilable_rooms = [x for x in range(1, no_of_room + 1) if x not in l]
            available_rooms = len(exact_avilable_rooms)
            try:
                room_count = int(data["room"])
                if room_count > available_rooms:
                    messages.info(req, f"Can't add more rooms than {available_rooms}")
                    return redirect(f"/booking-{id}")
            except (TypeError, ValueError):
                messages.info(req, "Invalid room count.")
                return redirect(f"/booking-{id}")


            #checking dates
            from_date = data["from_date"]
            to_date = data["to_date"]
            
            # Make sure from_date and to_date are valid before comparing
            if from_date and to_date:
                today = date.today()
                max_booking_date = today + timedelta(days=30)

                if (
                    to_date < from_date or   
                    to_date < today or      
                    from_date < today or    
                    from_date > max_booking_date or 
                    to_date > from_date + timedelta(days=30)  
                    ):
                    messages.info(req, 
                        "Invalid dates selected! 🚨\n"
                        "✔ Check-in date must be **today or later**.\n"
                        "✔ Check-out date must be **after** the check-in date.\n"
                        "✔ You can only book up to **30 days in advance**.\n"
                        "✔ The maximum stay duration is **30 days**.\n"
                        "📅 Please select valid dates and try again."
                    )
                    return redirect('/booking-1')
            else:
                # If dates are not provided, show an error
                messages.info(req, "Please enter valid dates.")
                return redirect(f'/booking-{id}')
            

            global adult, child

            #getting adults and child 
            adult={"room_1":req.POST.get('ra-1')}
            child={"room_1":req.POST.get('rc-1')}
            if 1<int(data["room"])<=available_rooms:
                for x in range(2, int(data["room"]) + 1):
                    adult[f"room_{x}"]=req.POST.get(f"adult_c-{x}")  
                    child[f"room_{x}"]=req.POST.get(f"child_c-{x}")

            #check data of adults and childs
            for x in adult:
                if int(adult.get(x))>room.space_for_adult:
                    messages.info(req,f'We have only {room.space_for_adult} for adult in this room')
                    return redirect(f"/booking-{id}")

            for x in child:
                if int(child.get(x))>room.space_for_child:
                    messages.info(req,f'can only add {room.space_for_child} child pr room')
                    return redirect(f"/booking-{id}")
            return redirect(f"/booking_details-{room.id}")  # Redirect after successful submission
        
        else:
            messages.info(req, "Please fill all the details correctly.")
    else:
        if req.user.is_authenticated:
            form = booking_details_form(initial=initial_data)  # Pre-fill form with initial values
        else:
            form=booking_details_form()
    # Make name and email fields readonly
    if req.user.is_authenticated:
        form.fields["name"].widget.attrs["readonly"] = True
        form.fields["email"].widget.attrs["readonly"] = True
    available_rooms =Rooms.objects.filter(room_type=room.room_type,room_availability=True).count()
    return render(req, "booking.html", {"room": room, "available_rooms": available_rooms, "form": form})   


def booking_details(request,id=0):
    global data, child,adult
    if data and child and adult:
        data1=data
        child2=child
        adult3=adult
        data=None
        child =None
        adult =None

    else:
        messages.info(request,"Sorry you can't access it")
        return redirect('home')


    try:
        room = R_D.objects.filter(id=id).first()
        if room is None:
            room = R_D.objects.first() 
        a=[]
        global t_a ,t_c
        t_a=0
        t_c=0
        for x in range(1,data1["room"]+1):
            tmp={"adults":adult3[f"room_{x}"],"children":child2[f"room_{x}"],"name":room.room_type,"room":x}
            t_a+=int(adult3[f"room_{x}"])
            t_c+=int(child2[f"room_{x}"])
            a.append(tmp)

        days = (data1["to_date"] - data1["from_date"]).days
        total=days*room.price*data1["room"]
        data1['total']=total
        if data1 and child2 and adult3:
            return render(request,'pay.html',{"room":room,"data":data1,"room_data":a,"total":total})
        else:
            messages.info(request,"you can't access this page")
            return redirect('/')
    except Exception as e:
        messages.info(request,f"you can't access this")
        return redirect('/')




def Booked(req):
    if not exact_avilable_rooms:
        return HttpResponse("No available rooms for booking.", status=400)

    # Get the available rooms
    available_rooms = exact_avilable_rooms[:]
    
    # Update room availability in the Rooms model
    room_objects = Rooms.objects.filter(room_availability=True, room_number__in=available_rooms)
    for room in room_objects:
        room.room_availability = False
        room.save()

    new=User_Booked_Room_Details(username=req.user.username if req.user.is_authenticated else data["name"],
                                 email=req.user.email if req.user.is_authenticated else data["email"],
                                 phone=data["phone"],
                                 room_type=data['room_name'],
                                 adults=t_a,
                                 child=t_c,
                                check_in =data["from_date"],
                                check_out=data['to_date'],
                                room_allocated=exact_avilable_rooms,
                                total_amount=data["total"],
                                Booked_on_date = date.today()
                                 )
    new.save()
    return HttpResponse("data submited successfully")




import threading
import time
from datetime import datetime, timedelta

task_scheduled = False 
def background_task():
    rooms = Rooms.objects.filter(room_availability=False).all()
    check_out_rooms = User_Booked_Room_Details.objects.filter(check_out__lte=date.today() + timedelta(days=1))
    room_no =[]
    for x in check_out_rooms:
        room_no.append(json.loads(x.room_allocated))
    room_no = sorted(set(np.array(room_no).flatten()))
    for room in rooms:
        if int(room.room_number) in room_no:  # Ensure consistent type
            room.room_availability = True
            room.save()

    
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

    task_scheduled = False  # Reset flag so it can run again



if not task_scheduled:
    task_thread = threading.Thread(target=schedule_task, daemon=True)
    task_thread.start()



# have to properly setup the booked route 
@csrf_exempt
def handel_request(request):
    pass