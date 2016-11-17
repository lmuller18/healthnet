from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import json

from appointment.models import *
from appointment.forms import *

from .validateAppointment import *

"""
View for creating a new appointment.
"""
@login_required
def NewAppointment( request ):

    user = request.user
    appointment_list = generateAppointmentList(user)
    calendarData = generateCalendar(appointment_list)
    # Present the initial page.
    if request.method == "GET":
        if Patient.objects.filter(user=user).exists():
            patient = Patient.objects.get(user=user)
            form = AppointmentForm( initial={
                'a_patient': patient.fName + ' ' + patient.lName,
            })

            return render( request, 'appointment/index.html', {
                'newForm': form,
                'patient': patient,
                'calendarData': calendarData,
                'appointment_list': appointment_list,
            })
        elif Doctor.objects.filter(user=user).exists():
            doctor = Doctor.objects.get(user=user)
            form = AppointmentForm( initial={
                'a_doctor': doctor.fName + ' ' + doctor.lName,
            })

            return render( request, 'appointment/index.html', {
                'newForm': form,
                'doctor': doctor,
                'calendarData': calendarData,
                'appointment_list': appointment_list,
            })
        elif Nurse.objects.filter(user=user).exists():
            form = AppointmentForm()
            return render( request, 'appointment/index.html', {
                'newForm': form,
                'calendarData': calendarData,
                'appointment_list': appointment_list,
            })
        else:
            return HttpResponseRedirect( reverse('login:login') )


    # The user submits the new appointment form.
    elif request.method == "POST":
        if Patient.objects.filter(user=user).exists():
            patient = Patient.objects.get(user=user)
            form = AppointmentForm( request.POST ) 

            if form.is_valid():
                doctor_email = form.cleaned_data.get('a_doctor')

                if not Doctor.objects.filter(email=doctor_email).exists():
                    return render( request, 'appointment/index.html', {
                        'newForm': form,
                        'patient': patient,
                        'calendarData': calendarData,
                        'appointment_list': appointment_list,
                    })

                doctor      = Doctor.objects.get(email=doctor_email)
                # -- We already have the patient --
                title       = form.cleaned_data.get('a_title')
                description = form.cleaned_data.get('a_description')
                date        = form.cleaned_data.get('a_date')
                starttime   = form.cleaned_data.get('a_starttime')
                endtime     = form.cleaned_data.get('a_endtime')

                # Make sure the appointment time is valid.
                if not isAppointmentValid(doctor, patient, date, starttime, endtime):
                    return render( request, 'appointment/index.html', {
                        'newForm': form,
                        'patient': patient,
                        'calendarData': calendarData,
                        'appointment_list': appointment_list,
                    })

                # Logging is done in scheduleAppointment
                appointment = Appointment.objects.scheduleAppointment(
                        doctor, patient, title, description,
                        date, starttime, endtime,
                )
                appointment.save()

                return HttpResponseRedirect( reverse('appointment:index') )
            else:
                return render( request, 'appointment/index.html', {
                    'newForm': form,
                    'patient': patient,
                    'calendarData': calendarData,
                    'appointment_list': appointment_list,
                })

        elif Doctor.objects.filter(user=user).exists():
            doctor = Doctor.objects.get(user=user)
            form = AppointmentForm( request.POST ) 

            if form.is_valid():
                patient_email = form.cleaned_data.get('a_patient')

                if not Patient.objects.filter(email=patient_email).exists():
                    return render( request, 'appointment/index.html', {
                        'newForm': form,
                        'doctor': doctor,
                        'calendarData': calendarData,
                        'appointment_list': appointment_list,
                    })

                # -- We already have the doctor -- 
                patient     = Patient.objects.get(email=patient_email)
                title       = form.cleaned_data.get('a_title')
                description = form.cleaned_data.get('a_description')
                date        = form.cleaned_data.get('a_date')
                starttime   = form.cleaned_data.get('a_starttime')
                endtime     = form.cleaned_data.get('a_endtime')

                # Make sure the appointment time is valid.
                if not isAppointmentValid(doctor, patient, date, starttime, endtime):
                    return render( request, 'appointment/index.html', {
                        'newForm': form,
                        'patient': patient,
                        'calendarData': calendarData,
                        'appointment_list': appointment_list,
                    })

                # Logging done in scheduleAppointment
                appointment = Appointment.objects.scheduleAppointment(
                        doctor, patient, title, description,
                        date, starttime, endtime)
                appointment.save()

                return HttpResponseRedirect( reverse('appointment:index') )
            else:
                return render( request, 'appointment/index.html', {
                    'newForm': form,
                    'doctor': doctor,
                    'calendarData': calendarData,
                    'appointment_list': appointment_list,
                })

        elif Nurse.objects.filter(user=user).exists():
            form = AppointmentForm( request.POST )

            if form.is_valid():
                doctor_email = form.cleaned_data.get('a_doctor')
                patient_email = form.cleaned_data.get('a_patient')
                
                if not Doctor.objects.filter(email=doctor_email).exists() or \
                        not Patient.objects.filter(email=patient_email).exists():
                    return render( request, 'appointment/index.html', {
                        'newForm': form,
                        'calendarData': calendarData,
                        'appointment_list': appointment_list,
                    })

                doctor = Doctor.objects.get(email=doctor_email)
                patient = Patient.objects.get(email=patient_email)
                title       = form.cleaned_data.get('a_title')
                description = form.cleaned_data.get('a_description')
                date        = form.cleaned_data.get('a_date')
                starttime   = form.cleaned_data.get('a_starttime')
                endtime     = form.cleaned_data.get('a_endtime')

                # Make sure the appointment time is valid.
                if not isAppointmentValid(doctor, patient, date, starttime, endtime):
                    return render( request, 'appointment/index.html', {
                        'newForm': form,
                        'patient': patient,
                        'calendarData': calendarData,
                        'appointment_list': appointment_list,
                    })

                appointment = Appointment.objects.scheduleAppointment(
                        doctor, patient, title, description,
                        date, starttime, endtime)
                appointment.save()

                return HttpResponseRedirect( reverse('appointment:index') )
            else:
                return render( request, 'appointment/index.html', {
                    'newForm': form,
                    'calendarData': calendarData,
                    'appointment_list': appointment_list,
                })

        # If not a patient, doctor, or nurse.
        else:
            return HttpResponseRedirect( reverse('login:login') )

    # Not GET or POST
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