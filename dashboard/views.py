from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Q
from appointment.models import *
from messaging.models import *
from prescriptions.models import *
from registration.forms import *
from testResult.models import *
from registration.models import *

from logs.views import get_queryset, get_statistics
import random
import json


@login_required
def generateDashboard(request):
    user = request.user
    if Doctor.objects.filter(user=user).exists():
        doctor = Doctor.objects.get(user=user)
        context = doctorDash(doctor)
        return render(request, 'dashboard/doctorDash.html', context)
    elif Patient.objects.filter(user=user).exists():
        patient = Patient.objects.get(user=user)
        context = patientDash(patient)
        return render(request, 'dashboard/patientDash.html', context)
    elif Nurse.objects.filter(user=user).exists():
        nurse = Nurse.objects.get(user=user)
        context = nurseDash(nurse)
        return render(request, 'dashboard/nurseDash.html', context)
    elif Admin.objects.filter(user=user).exists():
        admin = Admin.objects.get(user=user)
        context = adminDash(admin)
        return render(request, 'dashboard/adminDash.html', context)
    else:
        return HttpResponseRedirect('/login/')


@login_required
def patientDash(patient):
    # Upcoming appointments
    # Prescription List
    # Unread messages
    # Newest test result
    user = patient.user
    message_list = Message.objects.all().filter(Q(recipient=user, read=False)).filter(
        pubdate__lte=timezone.now()).order_by('-pubdate')
    prescription_list = Prescription.objects.all().filter(Q(p_patient=patient)).filter(
        p_expiration__gte=timezone.now()).order_by('p_expiration')
    appointment_list = Appointment.objects.all().filter(Q(a_patient=patient)).filter(
        a_date__gte=timezone.now()).order_by('a_starttime').order_by('a_date')
    result_list = Result.objects.all().filter(Q(t_patient=patient)).order_by('-t_created')
    calendarData = generateCalendar(appointment_list, "agendaWeek")
    context = {
        'form': PatientProfileForm(data=None, initial={
            'fName': patient.fName,
            'lName': patient.lName,
            'email': patient.email,
            'currHospital': patient.currHospital,
            'prefHospital': patient.prefHospital,
            'weight': patient.weight,
            'height': patient.height,
            'gender': patient.gender,
            'birthday': patient.birthday,
            'bloodtype': patient.bloodtype,
            'eName': patient.eName,
            'ePhone': patient.ePhone,
        }),
        'patient': patient,
        'message_list': message_list,
        'prescription_list': prescription_list,
        'appointment_list': appointment_list,
        'result_list': result_list,
        'calendarData': calendarData,
        'view': "agendaWeek",
    }
    return context

@login_required
def doctorDash(doctor):
    # Upcoming appointments
    # Prescription List
    # Unread messages
    # Newest test result
    user = doctor.user
    message_list = Message.objects.all().filter(Q(recipient=user, read=False)).filter(
        pubdate__lte=timezone.now()).order_by('-pubdate')
    prescription_list = Prescription.objects.all().filter(Q(p_doctor=doctor)).filter(
        p_created__lte=timezone.now()).order_by('-p_created')
    appointment_list = Appointment.objects.all().filter(Q(a_doctor=doctor)).filter(
        a_date__gte=timezone.now()).order_by('a_starttime').order_by('a_date')
    result_list = Result.objects.all().filter(t_doctor=doctor).order_by('-t_created')
    calendarData = generateCalendar(appointment_list, "agendaDay")
    context = {
        'message_list': message_list,
        'prescription_list': prescription_list,
        'appointment_list': appointment_list,
        'result_list': result_list,
        'calendarData': calendarData,
        'view': "agendaDay",
    }
    return context



@login_required
def nurseDash(nurse):
    # Upcoming appointments
    # Prescription List
    # Unread messages
    # Newest test result
    user = nurse.user
    message_list = Message.objects.all().filter(Q(recipient=user, read=False)).filter(
        pubdate__lte=timezone.now()).order_by('-pubdate')
    prescription_list = []
    for prescription in Prescription.objects.all():
            if prescription.p_patient.currHospital == nurse.hospital:
                prescription_list.append(prescription)
    result_list = []
    for result in Result.objects.all():
        if result.t_patient.currHospital == nurse.hospital:
            result_list.append(result)
    appointment_list = []
    for appt in Appointment.objects.all().order_by('a_starttime').order_by('a_date'):
        if appt.a_doctor.hospital == nurse.hospital:
            appointment_list.append(appt)
    calendarData = generateCalendar(appointment_list, "agendaDay")
    context = {
        'message_list': message_list,
        'prescription_list': prescription_list,
        'result_list': result_list,
        'calendarData': calendarData,
        'view': "agendaDay",
    }
    return context


@login_required
def adminDash(admin):
    user = admin.user
    logs = get_queryset()
    stats = get_statistics()
    prescriptionList = Prescription.objects.all()
    prescriptionData = []
    doctorPrescribed = {}
    prescriptionPrescribed = {}
    medNames = []
    color = {}

    patientList = Patient.objects.all()
    hospitals = {}
    hospitalData = []
    admission = {}
    hLabels = []
    hColor = {}
    for item in patientList:
        hospitals[str(item.currHospital)] = 0
    for item in patientList:
        hospitals[str(item.currHospital)] += 1
        if item.currHospital not in hLabels:
            hLabels.append(item.currHospital)
    for hospital in hospitals:
        total = 0
        for patient in patientList:
            admission[patient.currHospital] = 0
        for patient in Patient.objects.filter(currHospital=hospital):
            admission[patient.currHospital] += 1
            total += 1
        hospitalData.append({
            "Doctor": hospital,
            "freq": admission,
            "total": total,
        })
        admission = {}
    hospitalData = json.dumps(hospitalData)
    for h in hospitals:
        hColor[h] = "#%06x" % random.randint(0, 0xFFFFFF)

    for item in prescriptionList:
        if item.p_doctor.hospital == admin.hospital:
            doctorPrescribed[str(item.p_doctor)] = 0
    for item in prescriptionList:
        if item.p_doctor.hospital == admin.hospital:
            doctorPrescribed[str(item.p_doctor)] += 1
    for doc in doctorPrescribed:
        medNames = []
        doctor = Doctor.objects.get(email=doc)
        total = 0
        for prescription in prescriptionList:
            if prescription.p_doctor.hospital == admin.hospital:
                prescriptionPrescribed[prescription.p_prescription] = 0
        for prescription in prescriptionList.filter(p_doctor=doc):
            if prescription.p_doctor.hospital == admin.hospital:
                prescriptionPrescribed[prescription.p_prescription] += 1
                total += 1
        for med in prescriptionPrescribed:
            medNames.append(med)
        prescriptionData.append({
            "Doctor": "Dr. " + str(doctor.fName) + " " + str(doctor.lName),
            "freq": prescriptionPrescribed,
            "total": total
        })
        prescriptionPrescribed = {}
    prescriptionData = json.dumps(prescriptionData)
    for med in medNames:
        color[med] = "#%06x" % random.randint(0, 0xFFFFFF)
    context = {
        'logs': logs,
        'stats': stats,
        'prescriptionData': prescriptionData,
        'labels': medNames,
        'color': color,
        'hLabels': hLabels,
        'hospitalData': hospitalData,
        'hColor': hColor,
    }
    return context


def generateCalendar(appointment_list, view):
    calendarList = []
    for item in appointment_list:
        calendarList.append({
            "title": item.a_title,
            "start": str(item.a_date) + "T" + str(item.a_starttime),
            "end": str(item.a_date) + "T" + str(item.a_endtime),
            "allday": False,
        })
    return json.dumps(calendarList)