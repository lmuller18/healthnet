from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import *
from .forms import *
from messaging.models import *
from registration.models import *

import logging

logger = logging.getLogger('system')


@login_required
def PrescriptionView(request):
    user = request.user
    user_type = None
    isNurse = None
    canEdit = None
    if Patient.objects.filter(user=user).exists():
        patient_user = Patient.objects.get(user=user)
        list = Prescription.objects.filter(p_patient=patient_user).filter(
            p_created__lte=timezone.now()).order_by('-p_created')
    elif Doctor.objects.filter(user=user).exists():
        doctor_user = Doctor.objects.get(user=user)
        list = Prescription.objects.filter(p_doctor=doctor_user).filter(
            p_created__lte=timezone.now()).order_by('-p_created')
        user_type = doctor_user
        canEdit = True
    elif Nurse.objects.filter(user=user).exists():
        nurse_user = Nurse.objects.get(user=user)
        p_list = Prescription.objects.filter(p_created__lte=timezone.now()).order_by('-p_created')
        list = []
        for p in p_list:
            if p.p_patient.currHospital == nurse_user.hospital:
                list.append(p)
        isNurse = True
    else:
        return HttpResponseRedirect('/login/')

    return render(request, 'prescriptions/prescriptionDash.html', {
        'prescription_list': list,
        'doctor': user_type,
        'isNurse': isNurse,
        'canEdit': canEdit,
    })

@login_required
def viewPrescription(request, p_id):
    user = request.user
    canEdit = None
    isNurse = None
    user_type = None
    if Prescription.objects.filter(id=p_id).exists():
        if Patient.objects.filter(user=user).exists():
            patient_user = Patient.objects.get(user=user)
            list = Prescription.objects.filter(p_patient=patient_user).filter(
                p_created__lte=timezone.now()).order_by('-p_created')
            if not Prescription.objects.filter(p_patient=patient_user, id=p_id):
                return HttpResponseRedirect('/login/')
        elif Doctor.objects.filter(user=user).exists():
            doctor_user = Doctor.objects.get(user=user)
            list = Prescription.objects.filter(p_doctor=doctor_user).filter(
                p_created__lte=timezone.now()).order_by('-p_created')
            if not Prescription.objects.filter(p_doctor=doctor_user):
                return HttpResponseRedirect('/login/')
            user_type = doctor_user
            if Prescription.objects.filter(id=p_id, p_doctor=doctor_user).exists():
                canEdit = True
        elif Nurse.objects.filter(user=user).exists():
            nurse_user = Nurse.objects.get(user=user)
            if Prescription.objects.get(id=p_id).p_patient.currHospital != nurse_user.hospital:
                return HttpResponseRedirect('/prescriptions/')
            list = []
            for p in Prescription.objects.all():
                if p.p_patient.currHospital == nurse_user.hospital:
                    list.append(p)
            isNurse = True
        else:
            return HttpResponseRedirect('/login/')

        return render(request, 'prescriptions/prescriptionDash.html', {
            'prescription_list': list,
            'doctor': user_type,
            'view': Prescription.objects.get(id=p_id),
            'canEdit': canEdit,
            'isNurse': isNurse,
        })
    else:
        return HttpResponseRedirect('/prescriptions/')


@login_required
def New_Prescription(request):
    user = request.user
    if not Doctor.objects.filter(user=user).exists():
        return HttpResponseRedirect('/login/')
    doctor_user = Doctor.objects.get(user=user)
    list = Prescription.objects.filter(p_doctor=doctor_user).filter(
        p_created__lte=timezone.now()).order_by('-p_created')
    form = PrescriptionForm(request.POST or None, initial={
        'p_doctor': doctor_user.fName + ' ' + doctor_user.lName,
    })
    p_list = Patient.objects.all()
    if form.is_valid():
        #p_doctor = form.clean_data.get('p_doctor')
        patient = form.cleaned_data.get('p_patient')
        p_patient = Patient.objects.get(email=patient)
        p_prescription = form.cleaned_data.get('p_prescription')
        p_dose = form.cleaned_data.get('p_dose')
        p_units = form.cleaned_data.get('p_units')
        p_refills = form.cleaned_data.get('p_refills')
        p_expiration = form.cleaned_data.get('p_expiration')
        p_created = form.cleaned_data.get('p_created')

        logger.info("New Prescription: " + " " + doctor_user.fName + " " + doctor_user.lName + " " + p_patient.fName +
            " " + p_patient.lName + " " + p_prescription + " " + str(p_dose) + " " + str(p_units) + " " +
            str(p_refills) + " " + str(p_expiration) + " " + str(p_created))

        p = Prescription.objects.createPrescription(doctor_user, p_patient, p_prescription, p_expiration)
        p.p_patient = p_patient
        p.p_doctor = doctor_user
        p.p_prescription = p_prescription
        p.p_dose = p_dose
        p.p_units = p_units
        p.p_refills = p_refills
        p.p_expiration = p_expiration
        p.p_created = p_created
        p.save()

        recipient = User.objects.get(email=p_patient)
        message = Message.objects.createMessage(user, recipient, "New Prescription", "You have a new available prescription. ")
        message.link = "/prescriptions/" + (str(p.id) + "/view/")
        message.save()

        return HttpResponseRedirect('/prescriptions/')
    return render(request, 'prescriptions/prescriptionDash.html', {
        'newForm': form,
        'doctor': doctor_user,
        'prescription_list': list,
    })


@login_required
def Edit_Prescription(request, p_id):
    user = request.user
    if not Doctor.objects.filter(user=user).exists():
        return HttpResponseRedirect('/login/')
    doctor = Doctor.objects.get(user=user)

    list = Prescription.objects.filter(p_doctor=doctor).filter(
        p_created__lte=timezone.now()).order_by('-p_created')

    if Prescription.objects.filter(p_doctor=doctor, id=p_id).exists():
        p = Prescription.objects.get(p_doctor=doctor, id=p_id)
        form = PrescriptionEditForm(request.POST or None, initial={
            'p_doctor': doctor.fName + " " + doctor.lName,
            'p_patient': p.p_patient,
            'p_prescription': p.p_prescription,
            'p_dose': p.p_dose,
            'p_units': p.p_units,
            'p_refills': p.p_refills,
            'p_expiration': p.p_expiration,
            'p_created': p.p_created,
        })
        if form.is_valid():
            p_prescription = form.cleaned_data.get('p_prescription')
            p_dose = form.cleaned_data.get('p_dose')
            p_units = form.cleaned_data.get('p_units')
            p_refills = form.cleaned_data.get('p_refills')
            p_expiration = form.cleaned_data.get('p_expiration')
            p_created = form.cleaned_data.get('p_created')

            logger.info("Edit Prescription: " + " " + p.p_doctor.fName + " " + p.p_doctor.lName + " " +
            p.p_patient.fName + " " + " " + p.p_patient.lName + " " + p_prescription + " " + str(p_dose) +
            " " + str(p_units) + " " + str(p_refills) + " " + str(p_expiration) + " " + str(p_created))

            p.p_prescription = p_prescription
            p.p_dose = p_dose
            p.p_units = p_units
            p.p_refills = p_refills
            p.p_expiration = p_expiration
            p.save()

            recipient = User.objects.get(email=p.p_patient.email)
            message = Message.objects.createMessage(user, recipient, "Edited Prescription",
                                                    ("Your prescription of " + str(p) + " has been updated. "))
            message.link = "/prescriptions/" + str(p.id) + "/view/"
            message.save()

            return HttpResponseRedirect('/prescriptions/')
        return render(request, 'prescriptions/prescriptionDash.html', {
            'editForm': form,
            'prescription': p,
            'doctor': doctor,
            'patient': p.p_patient,
            'created': p.p_created,
            'prescription_list': list,
        })
    return HttpResponseRedirect('/prescriptions/')

@login_required()
def Delete_Prescription(request, p_id):
    user = request.user
    if not Doctor.objects.filter(user=user).exists():
        return HttpResponseRedirect('/login/')

    doctor = Doctor.objects.get(user=user)

    if Prescription.objects.filter(id=p_id).exists():
        p = Prescription.objects.get(id=p_id)
        recipient = User.objects.get(email=p.p_patient.email)
        Message.objects.createMessage(user, recipient, "Removed Prescription", ("Your prescription for " + str(p) +
                                                                                " has been removed. If you believe "
                                                                                "this has been in error, feel free "
                                                                                "to contact me through the HealthNet "
                                                                                "System"))
        p.delete()
        list = Prescription.objects.filter(p_doctor=doctor).filter(
            p_created__lte=timezone.now()).order_by('-p_created')
        return render(request, 'prescriptions/prescriptionDash.html', {
            'p' : p,
            'doctor': doctor,
            'prescription_list': list,
        })
    return HttpResponseRedirect('/prescriptions/')
