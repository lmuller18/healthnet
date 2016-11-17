from django import forms
from .models import *

"""
Search form. Yes, it's just a text box. This is done for consistency
    with the standard method of retrieving user input that is used
    across the project.
"""
class SearchForm(forms.Form):
    name = forms.CharField(label='Name', required=False)