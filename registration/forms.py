from django import forms
from .models import *
from django.forms.extras import SelectDateWidget

"""
Form for patient account creation
"""
class PatientRegForm(forms.Form):
    fName = forms.CharField(label='First Name', required=True)
    lName = forms.CharField(label='Last Name', required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Patient.objects.all().filter(email=email).exists():
            raise forms.ValidationError('Someone has already registered that email address')
        return email

"""
Form for admin-level account creation
"""
class AdminRegForm(forms.Form):
    types = {
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Nurse', 'Nurse')
    }
    accType = forms.ChoiceField(label='Account Type', choices=types, initial='Admin', required=True)
    
    fName = forms.CharField(label='First Name', required=True)
    lName = forms.CharField(label='Last Name', required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)
    
    hLabels = {
        ('Rochester General Hospital', 'Rochester General Hospital'),
        ('Rochester Private Hospital', 'Rochester Private Hospital'),
        ('Cleveland Clinic', 'Cleveland Clinic'),
        ('University of Pittsburgh Medical Center', 'University of Pittsburgh Medical Center'),
        ('UCLA Medical Center', 'UCLA Medical Center')
    }
    hospital = forms.ChoiceField(label='Hospital', choices=hLabels, initial='Rochester General Hospital', required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Patient.objects.all().filter(email=email).exists():
            raise forms.ValidationError('Someone has already registered that email address')
        elif Admin.objects.all().filter(email=email).exists():
            raise forms.ValidationError('Someone has already registered that email address')
        elif Doctor.objects.all().filter(email=email).exists():
            raise forms.ValidationError('Someone has already registered that email address')
        elif Nurse.objects.all().filter(email=email).exists():
            raise forms.ValidationError('Someone has already registered that email address')
        return email

"""
Form for patient profile creation/editing
"""
class PatientProfileForm(forms.Form):
    fName = forms.CharField(label='First Name', required=False)
    lName = forms.CharField(label='Last Name', required=False)
    email = forms.EmailField(label='Email', required=False)
    currHospital = forms.CharField(label='Current Hospital', required=False)

    hLabels = {
        ('Rochester General Hospital', 'Rochester General Hospital'),
        ('Rochester Private Hospital', 'Rochester Private Hospital'),
        ('Cleveland Clinic', 'Cleveland Clinic'),
        ('University of Pittsburgh Medical Center', 'University of Pittsburgh Medical Center'),
        ('UCLA Medical Center', 'UCLA Medical Center')
    }
    # the currHospital cannot be changed from these forms, so we only include hospital preference
    prefHospital = forms.ChoiceField(label='Preferred Hospital', choices=hLabels, initial='Rochester General Hospital', required=True)
    
    height = forms.IntegerField(label='Height', initial=0, min_value=0, required=True)
    weight = forms.IntegerField(label='Weight', initial=0, min_value=0, required=True)
    gLabels = {
        ('Male', 'Male'),
        ('Female', 'Female'),
    }
    gender = forms.ChoiceField(label='Gender', choices=gLabels, initial='Male',
                               widget=forms.Select(attrs={'class': 'smallDrop'}), required=True)
    birthday = forms.DateField(label='Birthday', initial='1990-01-01', required=True,
                                widget=SelectDateWidget(attrs={'class': 'smallDrop'},  years=range(2016, 1900, -1)))
    bLabels = {
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    }
    bloodtype = forms.ChoiceField(label='Blood Type', choices=bLabels, initial='A',
                                  widget=forms.Select(attrs={'class': 'smallDrop'}), required=True)
    
    eName = forms.CharField(label='Emergency Contact Name', required=True)
    ePhone = forms.CharField(label='Emergency Contact Phone Number', required=True)
    
"""
Form for patient hospital admission and discharge
"""
class PatientAdmissionForm(forms.Form):
    fName = forms.CharField(label='First Name', required=False)
    lName = forms.CharField(label='Last Name', required=False)
    
    hLabels = {
        ('Rochester General Hospital', 'Rochester General Hospital'),
        ('Rochester Private Hospital', 'Rochester Private Hospital'),
        ('Cleveland Clinic', 'Cleveland Clinic'),
        ('University of Pittsburgh Medical Center', 'University of Pittsburgh Medical Center'),
        ('UCLA Medical Center', 'UCLA Medical Center')
    }
    
    hospital = forms.ChoiceField(label='Hospital', choices=hLabels, initial='Rochester General Hospital', required=False)