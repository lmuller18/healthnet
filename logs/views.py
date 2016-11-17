from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


from .models import *
from registration.models import *
from prescriptions.models import *

"""
Main view for logs (index).
"""
@login_required
def LogView( request ):
    user = request.user

    if not Admin.objects.filter(user=user).exists():
        return HttpResponseRedirect(reverse('login:login'))

    return render(request, 'logs/index.html', {'queries': get_queryset(), 'statistics' : get_statistics()})

"""
Get all of the logs.
@return The list of all logs.
"""
def get_queryset():
    logs = list()
    f = open('activity.log', 'r')
    for line in f:
        logs.insert(0, Log(line))
    f.close()
    return logs;

def get_statistics():
    stats = list()
    patients = Patient.objects.all()
    prescriptions = Prescription.objects.all()

    #Creating each patient statistic
    for patient in patients:
        hospital = False
        for stat in stats:
            # Changed hospital to currHospital because hospital is not a field in the patient
            # object anymore and was causing a crash when trying to view logs/stats
            # added in this currHospital == None check because it was also causing a crash
            # if there was a patient in a hospital and a user not in a hospital
            # 
            if (stat.statistic == patient.currHospital):
                hospital = True
                stat.value += 1
        if not hospital:
            stats.append(Hospital_Statistic(patient.currHospital, 1))

    #Creating each prescription statistic
    for prescription in prescriptions:
        prescript = False
        for stat in stats:
            if stat.statistic == prescription.p_prescription:
                prescript = True
                stat.value+=1
                stat.average+=prescription.p_dose
                stat.units = prescription.p_units
        if not prescript:
            stats.append(Prescription_Statistic(prescription.p_prescription, 1, prescription.p_dose, prescription.p_units))

    #Computing the average of each prescription statistic
    for stat in stats:
        if type(stat) is Prescription_Statistic:
            stat.average/= stat.value

    return stats