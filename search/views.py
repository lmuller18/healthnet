from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login
from django.db.models import Q

from registration.models import *
from .forms import *

import logging

logger = logging.getLogger('system')

"""
Doctors and Nurses can search for patients
 - nurses are restricted to patients in their hospital
"""
@login_required
def SearchView(request):
    user = request.user
    
    if (user is None) or (user.is_anonymous()):
        return HttpResponseRedirect(reverse('login:login'))
    
    # queries must have a value to pass to render when form is not valid
    queries = None
    
    form = form = SearchForm(data=request.POST or None, initial={
        'name': "",
    })
        
    # redirect if user doesn't have required authorization
    if Doctor.objects.filter(user=user):
        if form.is_valid():
            names = form.cleaned_data.get('name').split(" ")
            
            queries = Patient.objects.filter( Q(fName__in=names) | Q(lName__in=names) )
            
            logger.info("Search for: " + str(names).strip('[]')
                + " by user: " + Doctor.objects.get(user=user).pk)
            
    elif Admin.objects.filter(user=user):
        if form.is_valid():
            names = form.cleaned_data.get('name').split(" ")

            queries = Patient.objects.filter( Q(fName__in=names) | Q(lName__in=names) )
            
            logger.info("Search for: " + str(names).strip('[]')
                + " by user: " + Admin.objects.get(user=user).pk)
            
    elif Nurse.objects.filter(user=user):
        if form.is_valid():
            names = form.cleaned_data.get('name').split(" ")
            
            # nurse is restricted to patients in their own hospital
            nHospital = Nurse.objects.get(user=user).hospital
            
            queries = Patient.objects.filter( Q(fName__in=names) | Q(lName__in=names), \
                Q(currHospital='Not in hospital') | Q(currHospital=nHospital) )
            
            logger.info("Search for: " + str(names).strip('[]')
                + " by user: " + Nurse.objects.get(user=user).pk)
    else:
        return HttpResponseRedirect(reverse('login:login'))
    
    return render(request, 'search/index.html', {'form': form, 'queries': queries})