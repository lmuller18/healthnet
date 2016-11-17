from django import forms
from registration.models import *


class NewMessageForm(forms.Form):
    # Editable Fields
    #recipient = forms.CharField(label='Recipient', widget=forms.TextInput(attrs={'placeholder': 'Recipient Email', 'class': 'expand'}),
    #                            required=False)

    recipient = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=False), empty_label=None, label='Recipient', widget=forms.Select(attrs={'class': 'chzn-select'}))

    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'expand'}),
                              required=True)
    content = forms.CharField(label='Message', widget=forms.Textarea(attrs={'placeholder': 'Type Message Here', 'class': 'expand'}),
                              required=True)

    def clean_recipient(self):
        recipient = self.cleaned_data.get('recipient')
        if not User.objects.all().filter(email=recipient).exists():
            raise forms.ValidationError('There are no users registered with that email address')
        return recipient


class RespondMessageForm(forms.Form):
    # Pre Filled In
    recipient = forms.CharField(label='Recipient', widget=forms.TextInput(attrs={'class': 'expand'}), required=False)

    # Editable fields
    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={'class': 'expand'}),  required=True)
    content = forms.CharField(label='Message', widget=forms.Textarea(attrs={'class': 'expand'}),  required=True)
