from django import forms
from datetime import datetime
from django.forms.extras import SelectDateWidget
from django.forms.utils import ErrorList
from registration.models import *

class TestResultForm(forms.Form):

    t_doctor = forms.CharField(label='Doctor',
                               required=False)
    t_patient = forms.ModelChoiceField(queryset=Patient.objects, empty_label=None, label='Patient',
                                       widget=forms.Select(attrs={'class': 'chzn-select'}))

    t_testname = forms.CharField(label='Test Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Test Name'}),
                                 required=True)

    t_result = forms.CharField(label='Result',
                               widget=forms.Textarea(attrs={'placeholder': 'Test Result'}),
                               required=True)

    t_created = forms.DateField(label='Date Created', initial=datetime.now, required=False,)

class EditForm(forms.Form):
    t_doctor = forms.CharField(label='Doctor',
                               required=False)
    t_patient = forms.ModelChoiceField(queryset=Patient.objects, empty_label=None, label='Patient',required=False)

    t_testname = forms.CharField(label='Test Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Test Name'}),
                                 required=True)

    t_result = forms.CharField(label='Result',
                               widget=forms.Textarea(attrs={'placeholder': 'Test Result'}),
                               required=True)

    t_created = forms.DateField(label='Date Created', initial=datetime.now, required=False,)