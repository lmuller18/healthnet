from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import json

from appointment.models import *
from appointment.forms import *

from .validateAppointment import *

"""
View for editing an existing appointment.
@param pk The numerical ID of the appointment.
"""
@login_required
def EditAppointment( request, pk ):
    # Get the user object.
    user = request.user
    appointment_list = generateAppointmentList(user)
    calendarData = generateCalendar(appointment_list)
    # Declare these for scope clarity
    patient = None
    doctor = None
    appointment = None
    isNurse = None
    
    # For each allowed user type, get their associated
    # appointment and the other person whom they are meeting with.
    if Patient.objects.filter(user=user).exists():

        patient = Patient.objects.get(user=user)
        
        if not Appointment.objects.filter(a_patient=patient, id=pk).exists():
            return HttpResponseRedirect( reverse('appointment:index') )

        appointment = Appointment.objects.get( a_patient=patient, id=pk )
        doctor = appointment.a_doctor
    elif Doctor.objects.filter(user=user).exists():

        doctor = Doctor.objects.get(user=user)

        if not Appointment.objects.filter(a_doctor=doctor, id=pk).exists():
            return HttpResponseRedirect( reverse('appointment:index') )

        appointment = Appointment.objects.get( a_doctor=doctor, id=pk )
        patient = appointment.a_patient
    elif Nurse.objects.filter(user=user).exists():
        if not Appointment.objects.filter(id=pk).exists():
            return HttpResponseRedirect( reverse('appointment:list') )
        appointment = Appointment.objects.get(id=pk)
        doctor = appointment.a_doctor
        patient = appointment.a_patient
        isNurse = True
    else:
        # If not a valid user type, redirect to login.
        return HttpResponseRedirect( reverse('login:login') )

    # Setup the form with the previous values as default.
    form = AppointmentForm( request.POST or None, initial={
        'a_doctor': doctor.fName + ' ' + doctor.lName,
        'a_patient': patient.fName + ' ' + patient.lName,
        'a_title':appointment.a_title,
        'a_description':appointment.a_description,
        'a_date':appointment.a_date,
        'a_starttime':appointment.a_starttime,
        'a_endtime':appointment.a_endtime,
    })
    
    # Make sure the form is valid so we can use the cleaned data.
    if form.is_valid():

        # Do not grab doctor or patient details since those are uneditable.
        title = form.cleaned_data.get('a_title')
        description = form.cleaned_data.get('a_description')
        date = form.cleaned_data.get('a_date')
        starttime = form.cleaned_data.get('a_starttime')
        endtime = form.cleaned_data.get('a_endtime')

        if not isAppointmentValid( doctor, patient, date, starttime, endtime, appointment ):
            return render(request, 'appointment/index.html', {
                'editForm': form,
                'appointment': appointment,
                'calendarData': calendarData,
                'appointment_list': appointment_list,
                'doctor': doctor,
                'patient': patient,
                'isNurse': isNurse,
            })

        appointment.update( title=title, description=description,
                            date=date, start=starttime, end=endtime )

        # Redirect back to the view for that appointment.
        redirect_url = reverse( 'appointment:view', kwargs={'pk':pk} )
        return HttpResponseRedirect( redirect_url )

    # Will render on initial get request and on invalid forms.
    else:
        return render(request, 'appointment/index.html', {
            'editForm': form,
            'appointment': appointment,
            'calendarData': calendarData,
            'appointment_list': appointment_list,
            'doctor': doctor,
            'patient': patient,
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