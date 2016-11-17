from registration.models import *
from django import forms
from django.forms.utils import ErrorList
from datetime import datetime
from django.forms.extras import SelectDateWidget




"""
Form for the creation of a new appointment.
"""
class AppointmentForm( forms.Form ):
    #a_doctor = forms.CharField( label='Doctor', max_length=200, required=False,
    #    widget=forms.TextInput( attrs={'placeholder': 'Doctor Email'}), )
    #a_patient = forms.CharField( label='Patient', max_length=200, required=False,
    #    widget=forms.TextInput( attrs={'placeholder': 'Patient Email'}), )

    a_doctor = forms.ModelChoiceField(queryset=Doctor.objects, empty_label=None, required=False, label='Doctor',
                                       widget=forms.Select(attrs={'class': 'chzn-select'}))
    a_patient = forms.ModelChoiceField(queryset=Patient.objects, empty_label=None, required=False, label='Patient',
                                       widget=forms.Select(attrs={'class': 'chzn-select'}))

    a_title = forms.CharField( label='Title', max_length=200, required=True, )

    a_description = forms.CharField( label='Description', max_length=1000,
        widget=forms.Textarea, )

    a_date = forms.DateField( label='Date', required=True, initial=datetime.today,
        widget=SelectDateWidget(attrs={'class': 'smallDrop'}) )

    a_starttime = forms.TimeField( label='Start Time', required=True,
        widget=forms.TextInput(attrs={'placeholder': '2:00 PM'}),
        input_formats=('%I:%M %p', '%H:%M', '%I:%M:%S %p', '%H:%M:%S'), )

    a_endtime = forms.TimeField( label='End Time', required=True, 
        widget=forms.TextInput(attrs={'placeholder': '2:30 PM'}),
        input_formats=('%I:%M %p', '%H:%M', '%I:%M:%S %p', '%H:%M:%S'), )

