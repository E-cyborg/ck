import os

n = input("Enter the path: ")
if os.path.exists(n):
    for i, x in enumerate(os.listdir(n)):
        file_path = os.path.join(n, x)  # Full path of the file
        if os.path.isfile(file_path):  # Ensure it's a file, not a directory
            if x.endswith(".jpg"):
                new_name = os.path.join(n, f'{i}.jpg')
                os.rename(file_path, new_name)
            elif x.endswith(".png"):
                new_name = os.path.join(n, f'{i}.png')
                os.rename(file_path, new_name)
else:
    print("The specified path does not exist.")





def booking(req,id):
    room= R_D.objects.filter(id=id).first() 
    today = date.today()
    three_months_ahead = today + timedelta(days=90)  # 3 months ahead
    tomorrow = today + timedelta(days=1)
    if room is None:
        room=R_D.objects.all()[0] 
    

    data={"available_rooms":Rooms.objects.filter(room_availability=True).all().count(),"today": today.strftime("%Y-%m-%d"),"tomorrow": tomorrow.strftime("%Y-%m-%d"),"three_months_ahead": three_months_ahead.strftime("%Y-%m-%d"),}
    return render(req,"booking.html",{"room":room,"data":data,})




import threading
import time
from datetime import datetime, timedelta

task_scheduled = False 
def background_task():
    rooms =Rooms.objects.filter(room_availability=False)

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
