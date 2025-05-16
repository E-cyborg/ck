from django.shortcuts import render
import threading
import time
from datetime import datetime, timedelta

def background_task():
    print(f"Task started at {datetime.now()}")
    # Your task logic here
    time.sleep(5)  # Simulate a task taking some time
    print("Task completed")

def schedule_task():
    """Schedules the task to run once every 24 hours."""
    while True:
        now = datetime.now()
        next_run = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        sleep_time = (next_run - now).total_seconds()

        print(f"Task scheduled to run at {next_run}")
        time.sleep(sleep_time)  
        background_task() 


def home(request):
    return render(request,"index.html",{})


task_thread = threading.Thread(target=schedule_task, daemon=True)
task_thread.start()
