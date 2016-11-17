from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from appointment.models import *

"""
View for listing out all of a user's appointments.
"""
@login_required
def ListAppointment( request ):
    # Get user token
    user = request.user

    appointment_list = None

    if Patient.objects.filter(user=user).exists():
        patient = Patient.objects.get(user=user)
        appointment_list = Appointment.objects.filter(a_patient=patient)\
                .order_by('a_date', 'a_starttime')
    elif Doctor.objects.filter(user=user).exists():
        doctor = Doctor.objects.get(user=user)
        appointment_list = Appointment.objects.filter(a_doctor=doctor)\
                .order_by('a_date', 'a_starttime')
    elif Nurse.objects.filter(user=user).exists():
        # The really long exclude is necessary for removing appointments today,
        # but have already ended (their end time is before the current time).
        # exclude currently has a bug where it can't take multiple parameters so
        # I had to use the method show below by excluding a filter.
        appointment_list = Appointment.objects.all()\
                .exclude( a_date__gte=(datetime.today()+timedelta(days=7)) )\
                .exclude( a_date__lt=datetime.today() )\
                .exclude( id__in=Appointment.objects.filter(a_date=datetime.today(), a_endtime__lt=datetime.now()) )\
                .order_by('a_date', 'a_starttime')

    else:
        return HttpResponseRedirect( reverse('login:login') )


    return render( request, 'appointment/list.html', {
        'appointment_list': appointment_list
    })
