from django.urls import path
from registration import views

urlpatterns = [
    path("login", views.loginUser, name="login"),  # Login view
    path("sign", views.signin_user, name="sign"),    # Signup (or signin) view
    path("logout/", views.logout_user, name="logout"),    # Signup (or signin) view
    path("user_dashboard", views.user_dashboard, name="user_dashboard"),
]
