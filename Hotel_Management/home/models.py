from django.db import models
from django.utils.timezone import now 
from django.contrib.auth.models import User


class R_D(models.Model):
    room_type = models.CharField(max_length=50, unique=True)  # Ensuring unique room types for proper ForeignKey
    room_description = models.CharField(max_length=500)
    space_for_adult = models.IntegerField()
    space_for_child = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.room_type} - {self.room_description} (Adults: {self.space_for_adult}, Children: {self.space_for_child}, Price: {self.price})"


class Rooms(models.Model):
    room_type = models.ForeignKey(
        "R_D",
        on_delete=models.CASCADE,
        related_name="rooms",
        to_field="room_type"
    )
    room_number = models.IntegerField()
    room_availability = models.BooleanField()
    class Meta:
        unique_together = ("room_type", "room_number")  # Ensures unique room numbers per type

    def __str__(self):
        return f"{self.room_type} - Room {self.room_number} - {'Available' if self.room_availability else 'Not Available'}"


class Comment(models.Model):
    room_type = models.ForeignKey("R_D", on_delete=models.CASCADE,to_field="room_type")
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')  # ForeignKey to 'User' model
    comm_date = models.DateField(default=now)
    message = models.TextField()

    def __str__(self):
        return f"{self.username} - {self.room_type} -{self.message} - {self.comm_date}"
    
class Contact(models.Model):
    username = models.CharField(max_length=50, blank=False, null=False)
    email =models.EmailField(max_length=254)
    subject = models.CharField(max_length=150)
    message = models.CharField( max_length=1000)
    date = models.DateField(default=now)

    def __str__(self):
        return f"{self.username}- {self.email} - {self.subject} - {self.message} -{self.date}"
    
class temp(models.Model):
    username= models.CharField(max_length=255)
    rooms=models.ForeignKey("R_D", on_delete=models.CASCADE,to_field="room_type")


class User_Booked_Room_Details(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=12, blank=True, null=True)  
    room_type = models.ForeignKey(
        "R_D",
        on_delete=models.CASCADE,
        to_field="room_type",
        related_name="booked_rooms"
    )
    adults = models.IntegerField()
    child = models.IntegerField(default=0, null=True, blank=True)  
    check_in = models.DateField()
    check_out = models.DateField()
    room_allocated = models.JSONField(default=list)  # Stores list of room numbers
    Booked_on_date = models.DateField(auto_now_add=True)  # Auto set when created
    total_amount = models.IntegerField()

    def __str__(self):
        return (f"Booking by {self.username} | Email: {self.email} | Phone: {self.phone or 'N/A'} | "
                f"Room Type: {self.room_type} | "
                f"Rooms Allocated: {self.room_allocated} | Adults: {self.adults} | Children: {self.child} | "
                f"Check-in: {self.check_in} | Check-out: {self.check_out} | "
                f"Total Amount: ${self.total_amount} | Booked on: {self.Booked_on_date}")
