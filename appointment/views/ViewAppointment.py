from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import json

from appointment.models import *
from appointment.forms import *

"""
View for viewing an existing appointment.
@param pk The numerical ID of the appointment.
"""
@login_required
def ViewAppointment( request, pk ):

    # Get the user token.
    user = request.user
    appointment_list = generateAppointmentList(user)
    calendarData = generateCalendar(appointment_list)
    isNurse = None

    if Patient.objects.filter(user=user).exists():
        patient = Patient.objects.get(user=user)
        if not Appointment.objects.filter(a_patient=patient, id=pk).exists():
            return HttpResponseRedirect( reverse('login:login') )
    elif Doctor.objects.filter(user=user).exists():
        doctor = Doctor.objects.get(user=user)
        if not Appointment.objects.filter(a_doctor=doctor, id=pk).exists():
            return HttpResponseRedirect( reverse('login:login') )
    elif Nurse.objects.filter(user=user).exists():
        if not Appointment.objects.filter(id=pk).exists():
            return HttpResponseRedirect( reverse('login:login') )
        isNurse = True
    else:
        return HttpResponseRedirect( reverse('login:login') )

    appointment = Appointment.objects.get(id=pk)

    form = AppointmentForm( initial={
        'a_doctor':appointment.a_doctor,
        'a_patient': appointment.a_patient,
        'a_title':appointment.a_title,
        'a_description':appointment.a_description,
        'a_date':appointment.a_date,
        'a_starttime':appointment.a_starttime,
        'a_endtime':appointment.a_endtime,
    })
    
    return render(request, 'appointment/index.html', {
        'calendarData': calendarData,
        'appointment_list': appointment_list,
        'view': appointment,
        'isNurse': isNurse,
    })


def generateAppointmentList(user):
    # If the user is a patient.
    if Patient.objects.filter(user=user).exists():
        patient = Patient.objects.get(user=user)
        appointment_list = Appointment.objects.filter(a_patient=patient)

    # If the user is a doctor
    elif Doctor.objects.filter(user=user).exists():
        doctor = Doctor.objects.get(user=user)
        appointment_list = Appointment.objects.filter(a_doctor=doctor)
    elif Nurse.objects.filter(user=user).exists():
        nurse = Nurse.objects.get(user=user)
        appointment_list = []
        for a in Appointment.objects.all():
            if a.a_doctor.hospital == nurse.hospital:
                appointment_list.append(a)
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