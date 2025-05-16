from django.contrib import admin
from django.urls import path,include
from home import views


urlpatterns = [
    path('',views.home,name="home"),
    path('room',views.rooms,name="room"),
    path('gallery',views.gallery,name="gallery"),
    path('contact',views.contact,name="contact"),
    path('description_room-<id>',views.details_room,name="details_room"),
    path('page_not_found',views.page_not_found,name="404"),
    path('booking-<id>',views.booking,name="booking"),
    path('booking_details-<id>',views.booking_details,name="book_d"),
    path("handle_request",views.handel_request,name="handle_request"),
]
