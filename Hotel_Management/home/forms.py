from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django import forms
from datetime import date , timedelta
from dateutil.relativedelta import relativedelta
from django.core.validators import MinValueValidator, MaxValueValidator




class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model =User
        fields= ["username","email","password1","password2"]

class comments_form(forms.Form):
    message = forms.CharField( max_length=500, required=True)

class Contact_form(forms.Form):
    username = forms.CharField(required=True)
    email= forms.EmailField( required=True)
    subject = forms.CharField(required=False)
    message = forms.CharField(
        widget=forms.Textarea(attrs={
        "placeholder":"Enter you message",
        "style": "height:75px; max-height: 200px; min-height: 100px; overflow: auto;"
    }),label=None, max_length=1000, required=True)



class booking_details_form(forms.Form):
    TITLE_CHOICES = [
        ("Mr.", "Mr."),
        ("Mrs./Ms.", "Mrs./Ms."),
        ("Other", "Other"),
    ]
    title = forms.ChoiceField(
        choices=TITLE_CHOICES, 
        widget=forms.RadioSelect(attrs={'class':"radio-group"}), 
        required=True, 
        label="Title"
    )
    name = forms.CharField(max_length=70, required=True)
    email =forms.EmailField( required=True)
    phone = forms.RegexField(
        regex=r'^\d{10}$',  # Allows exactly 10 digits
        error_messages={"invalid": "Enter a valid 10-digit phone number."},
        required=True
    )
    COUNTRY_CHOICES = [
        ("India", "India"),
        ("United States", "United States"),
        ("United Kingdom", "United Kingdom"),
        ("Canada", "Canada"),
        ("Australia", "Australia"),
    ]

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select,
        required=True,
        initial="India"  # Set default value
    )

    # Calculate tomorrow's date
    tomorrow = date.today() + relativedelta(days=+1)
    
    # Calculate 3 months from today
    three_months_later = date.today() + relativedelta(months=+3)
    
    # From date field: Min is today, Max is 3 months from today
    from_date = forms.DateField(
        initial=date.today(),  # Set default to today
        required=False,
        widget=forms.DateInput(attrs={'type': 'date','class':'form-control','min':date.today(),'max':three_months_later,'id':'from_date'}),
        label="From Date",
        validators=[
            MinValueValidator(date.today()),  # Minimum value is today
            MaxValueValidator(three_months_later)  # Maximum value is 3 months from today
        ]
    )
    
    # To date field: Min is tomorrow, Max is 3 months from today
    TO_date = forms.DateField(
        initial=tomorrow,  # Set default to tomorrow
        required=False,
        widget=forms.DateInput(attrs={'type': 'date','class':'form-control','min':date.today(),'max':three_months_later,'id':'to_date'}),
        label="To Date",
        validators=[
            MinValueValidator(tomorrow),  # Minimum value is tomorrow
            MaxValueValidator(three_months_later)  # Maximum value is 3 months from today
        ]
    )
