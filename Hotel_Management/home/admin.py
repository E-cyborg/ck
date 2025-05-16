from django.contrib import admin
from .models import R_D , Rooms,Comment,Contact,User_Booked_Room_Details
# Register your models here.
admin.site.register(R_D)

admin.site.register(Comment) 
# class RoomAdmin(admin.ModelAdmin):
#     list_display=('room_type','room_number','room_availability','from_date','to_date')
#     list_filter = ('from_date',)
#     search_fields = ('room_type','room_number','room_availability')
#     ordering=('-form_date',)

admin.site.register(Rooms) #admin.site.register(Rooms,RoomAdmin)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'subject', 'message', 'date')  # Columns in admin panel
    list_filter = ('date',)  # Add filter on date
    search_fields = ('username', 'email', 'subject', 'message')  # Search bar functionality
    ordering = ('-date',)  # Sort by latest date first
admin.site.register(Contact,ContactAdmin)

class UserBookedRoomDetailsAdmin(admin.ModelAdmin):
    list_display = (
        "username", "email", "phone", "room_type", "room_allocated",
        "adults", "child", "check_in", "check_out", "Booked_on_date", "total_amount"
    )  # Columns to display

    list_filter = ("room_type", "check_in", "check_out", "Booked_on_date")  # Filter options

    search_fields = ("username", "email", "phone", "room_type__room_type", "room_allocated")  # Fields to search

    ordering = ("-Booked_on_date",)  # Order by most recent bookings

    date_hierarchy = "check_in"  # Adds date-based navigation

    readonly_fields = ("Booked_on_date", "room_allocated")  # Make certain fields read-only

    def formatted_room_allocated(self, obj):
        """Format room_allocated for better readability."""
        return ", ".join(map(str, obj.room_allocated)) if obj.room_allocated else "N/A"

    formatted_room_allocated.short_description = "Rooms Allocated"

admin.site.register(User_Booked_Room_Details, UserBookedRoomDetailsAdmin)
