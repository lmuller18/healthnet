from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import json
import os

from appointment.models import *

"""
Main view for appointments (index).
"""
@login_required
def AppointmentView( request ):
 
    user = request.user # Get the user object
    
    appointment_list = None
    isNurse = None

    # If the user is a patient.
    if Patient.objects.filter(user=user).exists():
        patient = Patient.objects.get(user=user)
        appointment_list = Appointment.objects.filter( a_patient=patient )

    # If the user is a doctor
    elif Doctor.objects.filter(user=user).exists():
        doctor = Doctor.objects.get(user=user)
        appointment_list = Appointment.objects.filter( a_doctor=doctor )

    # If the user is a nurse, they should be redirected
    # from the calendar to the list view (since they are
    # not allowed to see the calendar view).
    elif Nurse.objects.filter(user=user).exists():
        nurse = Nurse.objects.get(user=user)
        appointment_list = []
        for a in Appointment.objects.all():
            if a.a_doctor.hospital == nurse.hospital:
                appointment_list.append(a)
        isNurse = True

    # If the user is none of the above user types.
    else:
        # Reverse to index of login page.
        return HttpResponseRedirect( reverse('login:login') )
    
    
    # Using list of appointment objects, this will write a javascript file
    # that will be used to generate a calendar for the user.

    calendarData = generateCalendar(appointment_list)
    context = {
        'calendarData': calendarData,
        'appointment_list': appointment_list,
        'isNurse': isNurse
    }
    return render(request, 'appointment/index.html', context)


def generateCalendar(appointment_list):
    calendarList = []
    for item in appointment_list:
        calendarList.append({
            "title": item.a_title,
            "start": str(item.a_date) + "T" + str(item.a_starttime),
            "end": str(item.a_date) + "T" + str(item.a_endtime),
            "url": '/appointment/' + str(item.id) + "/view/",
            "allday": False,
        })
    return json.dumps(calendarList)
