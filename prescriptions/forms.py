from django import forms
from django.forms.extras import SelectDateWidget
from registration.models import *


class PrescriptionForm(forms.Form):
    error_css_class = 'error'
    p_doctor = forms.CharField(label='Prescribing Doctor',
                               widget=forms.TextInput(attrs={'placeholder': 'will be set to curDoctor'}),
                               required=False)
    #p_patient = forms.CharField(label='Patient',
    #                            widget=forms.TextInput(attrs={'placeholder': 'Patient Email'}),
    #                            required=False)

    p_patient = forms.ModelChoiceField(queryset=Patient.objects, empty_label=None, label='Patient', widget=forms.Select(attrs={'class': 'chzn-select'}))
    p_prescription = forms.CharField(label='Medication', required=True)
    p_dose = forms.IntegerField(label='Dosage', initial=0, required=True)
    labels = (
        ('mg', 'mg'),
        ('cc', 'cc'),
    )
    p_units = forms.ChoiceField(label='Units', choices=labels, widget=forms.Select(attrs={'class': 'smallDrop'}),
                                initial='mg', required=True)
    p_refills = forms.IntegerField(label='Refills', initial=0, required=True)
    p_expiration = forms.DateField(label='Expiration Date', initial=datetime.today, required=True,
                                   widget=SelectDateWidget(attrs={'class': 'smallDrop'}))
    p_created = forms.DateField(label='Date Created', initial=datetime.today, required=True,
                                widget=SelectDateWidget(attrs={'class': 'smallDrop'}))

    def clean_p_patient(self):
        p_patient = self.cleaned_data.get('p_patient')
        if not Patient.objects.all().filter(email=p_patient).exists():
            raise forms.ValidationError('Not a valid Patient email address')
        return p_patient

    def clean_p_dose(self):
        p_dose = self.cleaned_data.get('p_dose')
        if p_dose <= 0:
            raise forms.ValidationError('Not a valid dose amount')
        return p_dose


class PrescriptionEditForm(forms.Form):
    p_doctor = forms.CharField(label='Prescribing Doctor',
                               widget=forms.TextInput(attrs={'placeholder': 'will be set to curDoctor'}),
                               required=False)
    p_patient = forms.CharField(label='Patient',
                                widget=forms.TextInput(attrs={'placeholder': 'Patient Email'}),
                                required=False)
    p_created = forms.DateField(label='Date Created', initial=datetime.today, required=False,
                                widget=SelectDateWidget(attrs={'class': 'smallDrop'}))
    p_prescription = forms.CharField(label='Medication', required=True)
    p_dose = forms.IntegerField(label='Dosage', initial=0, required=True)
    labels = (
        ('mg', 'mg'),
        ('cc', 'cc'),
    )
    p_units = forms.ChoiceField(label='Units', choices=labels, widget=forms.Select(attrs={'class': 'smallDrop'}),
                                initial='mg', required=True)
    p_refills = forms.IntegerField(label='Refills', initial=0, required=True)
    p_expiration = forms.DateField(label='Expiration Date', initial=datetime.today, required=True,
                                   widget=SelectDateWidget(attrs={'class': 'smallDrop'}))

    def clean_p_dose(self):
        p_dose = self.cleaned_data.get('p_dose')
        if p_dose <= 0:
            raise forms.ValidationError('Not a valid dose amount')
        return p_dose
