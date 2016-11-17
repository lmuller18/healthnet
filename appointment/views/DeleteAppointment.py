from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import json

from appointment.models import *

"""
View for deleting an existing appointment.
"""
@login_required
def DeleteAppointment( request, pk ):

    # Get the user token.
    user = request.user
    # The user is a patient.
    if Patient.objects.filter(user=user).exists():

        patient = Patient.objects.get(user=user)
        
        if Appointment.objects.filter(a_patient=patient, id=pk).exists():
            appointment = Appointment.objects.get(id=pk)
            appointment.remove() # Also logs the deletion
            appointment_list = generateAppointmentList(user)
            calendarData = generateCalendar(appointment_list)
            return render(request, 'appointment/index.html', {
                'p': appointment,
                'calendarData': calendarData,
                'appointment_list': appointment_list,
            })
        else:
            return HttpResponseRedirect( reverse('login:login') )
    # The user is a doctor.
    elif Doctor.objects.filter(user=user).exists():

        doctor = Doctor.objects.get(user=user)
        
        if Appointment.objects.filter(a_doctor=doctor, id=pk).exists():
            appointment = Appointment.objects.get(id=pk)
            appointment.remove() # Also logs the deletion
            appointment_list = generateAppointmentList(user)
            calendarData = generateCalendar(appointment_list)
            return render(request, 'appointment/index.html', {
                'p': appointment,
                'calendarData': calendarData,
                'appointment_list': appointment_list,
            })
        else:
            return HttpResponseRedirect( reverse('login:login') )
    # Nurses can't delete appointments.
    elif Nurse.objects.filter(user=user).exists():
        return HttpResponseRedirect( reverse('appointment:list') )
    # The user is none of the above types.
    else:
        return HttpResponseRedirect( reverse('login:login') )


def generateAppointmentList(user):
    # If the user is a patient.
    if Patient.objects.filter(user=user).exists():
        patient = Patient.objects.get(user=user)
        appointment_list = Appointment.objects.filter(a_patient=patient)

    # If the user is a doctor
    elif Doctor.objects.filter(user=user).exists():
        doctor = Doctor.objects.get(user=user)
        appointment_list = Appointment.objects.filter(a_doctor=doctor)
    else:
        appointment_list = None
    return appointment_list

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
