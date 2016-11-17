from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from prescriptions.models import *
from testResult.models import *

from .models import *
from .forms import *

import logging

logger = logging.getLogger('system')


"""
Patient registration page (index).
"""
def PatientReg(request):
    form = PatientRegForm(data=request.POST or None)
    
    user = request.user

    if not user.is_anonymous():
        return HttpResponseRedirect(reverse('login:login'))

    # is_valid() is causing a crash when user doesn't exist
    if form.is_valid():
        fName = form.cleaned_data.get('fName')
        lName = form.cleaned_data.get('lName')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        patient = Patient.objects.createPatient(fName, lName, email, password)
        patient.user.first_name = fName
        patient.user.last_name = lName
        patient.user.save()
        patient.save()

        user = authenticate(username=patient.email, password=password)
        login(request, user)

        logger.info("New User: First Name: " + str(fName) + " Last Name: " + str(lName) + " Email: " + str(email))

        return HttpResponseRedirect(reverse('registration:edit'))
    
    return render(request, 'registration/index.html', {'form': form})


"""
View that shows patient profile.
It is built from a form, but the form is not editable.
"""
@login_required
def PatientProfileView(request, key=None):
    user = request.user
    
    if (user is None) or (user.is_anonymous()):
        return HttpResponseRedirect(reverse('login:login'))
    
    # if someone is in a hospital, nurse can't discharge them
    nurseAdmit = False
    # certain conditions must be met for transfer permissions
    docCanTransfer = False
    # the optional key arg is only used when a non-patient is viewing a profile
    isPatient = False
    # admins only have transfer access
    isAdmin = False
    isDoctor = None
    prescription_list = None
    result_list = None
    
    # redirect if user isn't authorized for access
    if Patient.objects.filter(user=user).exists():
        isPatient = True
        
        patient = Patient.objects.get(user=user)
    
    elif Doctor.objects.filter(user=user).exists():
        if key is None:
            return HttpResponseRedirect(reverse('login:login'))
        
        patient = Patient.objects.get(pk=key)
        
        if patient.currHospital != 'Not in hospital':
            if Doctor.objects.get(user=user).hospital != patient.currHospital:
                docCanTransfer = True
        isDoctor = Doctor.objects.get(user=user)
        if Prescription.objects.filter(p_patient=patient).exists():
            prescription_list = Prescription.objects.filter(p_patient=patient)
        if Result.objects.filter(t_patient=patient).exists():
            result_list = Result.objects.filter(t_patient=patient)

    elif Nurse.objects.filter(user=user).exists():
        nurseAdmit = True
        
        if key is None:
            return HttpResponseRedirect(reverse('login:login'))
        
        patient = Patient.objects.get(pk=key)
        isDoctor = True
        nurse = Nurse.objects.get(user=user)
        prescription_list = []
        for p in Prescription.objects.all():
            if p.p_patient.currHospital == nurse.hospital:
                prescription_list.append(p)
        result_list = []
        for t in Result.objects.all():
            if t.t_patient.currHospital == nurse.hospital:
                result_list.append(t)
        if Nurse.objects.get(user=user).hospital != patient.currHospital:
            nurseAdmit = False
            
            if patient.currHospital != 'Not in hospital':
                return HttpResponseRedirect(reverse('login:login'))
    
    elif Admin.objects.filter(user=user).exists():
        if key is None:
            return HttpResponseRedirect(reverse('login:login'))
        
        patient = Patient.objects.get(pk=key)
        
        isAdmin = True
        
    else:
        return HttpResponseRedirect(reverse('login:login'))
    
    form = PatientProfileForm(data=request.POST or None, initial={
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
    })

    return render(request, 'registration/profile.html', {
        'form': form,
        'patient': patient,
        'isPatient': isPatient,
        'nurseAdmit': nurseAdmit,
        'isAdmin': isAdmin,
        'docCanTransfer': docCanTransfer,
        'doctor': isDoctor,
        'prescription_list': prescription_list,
        'result_list': result_list,
    })


"""
Editable view of the patient profile
"""
@login_required
def PatientProfileEdit(request, key=None):
    user = request.user
    
    if (user is None) or (user.is_anonymous()):
        return HttpResponseRedirect(reverse('login:login'))
    
    # redirect if patient isn't logged in
    if not Patient.objects.filter(user=user):
        if Doctor.objects.filter(user=user):
            if key is None:
                return HttpResponseRedirect(reverse('login:login'))

            patient = Patient.objects.get(pk=key)
            
        elif Nurse.objects.filter(user=user):
            if key is None:
                return HttpResponseRedirect(reverse('login:login'))
            
            patient = Patient.objects.get(pk=key)
            
            if not ( Nurse.objects.get(user=user).hospital == patient.currHospital ):
                return HttpResponseRedirect(reverse('login:login'))
            
        else:
            return HttpResponseRedirect(reverse('login:login'))
    else:
        patient = Patient.objects.get(user=user)
    
    form = PatientProfileForm(data=request.POST or None, initial={
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
    })
    
    if form.is_valid():
        hospital = form.cleaned_data.get('prefHospital')
        weight = form.cleaned_data.get('weight')
        height = form.cleaned_data.get('height')
        gender = form.cleaned_data.get('gender')
        birthday = form.cleaned_data.get('birthday')
        bloodtype = form.cleaned_data.get('bloodtype')
        eName = form.cleaned_data.get('eName')
        ePhone = form.cleaned_data.get('ePhone')
        
        patient.prefHospital = hospital
        patient.weight = weight
        patient.height = height
        patient.gender = gender
        patient.bloodtype = bloodtype
        patient.birthday = birthday
        patient.eName = eName
        patient.ePhone = ePhone
        patient.save()
        
        logger.info("Update Profile: Hospital: " + str(hospital) + " Weight: " + str(weight) + " Height: " 
        	+ str(height) + " Gender: " + str(gender) + " Birthday: " + str(birthday) + " Blood type: "
            + str(bloodtype) + " Emergency Contact Name: "
            + str(eName) + " Emergency Contact Phone Number: " + str(ePhone) )

        return HttpResponseRedirect('/registration/profile/' + patient.pk + '/')
    
    return render(request, 'registration/edit.html', {'form': form})


"""
View for admitting and discharging patients
"""
@login_required
def PatientAdmissionView(request, key):
    user = request.user
    
    if (user is None) or (user.is_anonymous()):
        return HttpResponseRedirect(reverse('login:login'))

    if Doctor.objects.filter(user=user):
        userPk = Doctor.objects.get(user=user).pk
        
        patient = Patient.objects.get(pk=key)
        
        isNurse = False

    elif Nurse.objects.filter(user=user):
        userPk = Nurse.objects.get(user=user).pk
        
        patient = Patient.objects.get(pk=key)

        isNurse = True
        
        if patient.currHospital != 'Not in hospital':
                return HttpResponseRedirect(reverse('login:login'))

    else:
        return HttpResponseRedirect(reverse('login:login'))
    
    if patient.currHospital != 'Not in hospital':
        isAdmitted = True
    else:
        isAdmitted = False
    
    form = PatientAdmissionForm(data=request.POST or None, initial={
        'fName': patient.fName,
        'lName': patient.lName,
        'hospital': patient.currHospital,
    })
        
    if form.is_valid():
        if isAdmitted:
            hospital = 'Not in hospital'
            prevHospital = patient.currHospital
        elif isNurse:
            hospital = Nurse.objects.get(user=user).hospital
        else:
            hospital = form.cleaned_data.get('hospital')

        if not isAdmitted:
            logger.info('Admit Patient: ' + patient.pk + ' Into: ' + hospital + ' Done By: ' + userPk )
        else:
            logger.info('Discharge Patient: ' + patient.pk + ' From: ' + prevHospital + ' Done By: ' + userPk )
        
        patient.currHospital = hospital
        patient.save()
        
        return HttpResponseRedirect('/registration/profile/' + patient.pk + '/')
    
    return render(request, 'registration/admit.html', {'form': form, 'isAdmitted': isAdmitted, 'isNurse': isNurse})


"""
View for transfering patients
"""
@login_required
def PatientTransferView(request, key):
    user = request.user

    if (user is None) or (user.is_anonymous()):
        return HttpResponseRedirect(reverse('login:login'))

    if Doctor.objects.filter(user=user):
        isAdmin = False
        userPk = Doctor.objects.get(user=user).pk
        
    elif Admin.objects.filter(user=user):
        isAdmin = True
        userPk = Admin.objects.get(user=user).pk
        
    else:
        return HttpResponseRedirect(reverse('login:login'))
    
    patient = Patient.objects.get(pk=key)
    
    form = PatientAdmissionForm(data=request.POST or None, initial={
        'fName': patient.fName,
        'lName': patient.lName,
        'hospital': patient.currHospital,
    })
    
    if form.is_valid():
        if not isAdmin:
            hospital = Doctor.objects.get(user=user).hospital
        else:
            hospital = form.cleaned_data.get('hospital')

        logger.info('Transfer Patient: ' + patient.pk + ' Into: ' + hospital + ' Done By: ' + userPk)
        
        patient.currHospital = hospital
        patient.save()
        
        return HttpResponseRedirect('/registration/profile/' + patient.pk + '/')
    
    return render(request, 'registration/transfer.html', {'form': form, 'isAdmin': isAdmin})


"""
Admin-level registration page. Admin accounts can create other users
    (admins, nurses, doctors). Since only admins can access this,
    there must be at least one admin created from the django admin.
"""
@login_required
def AdminReg(request):
    user = request.user
    
    # redirect if admin isn't logged in
    if (user is None) or (user.is_anonymous()):
        return HttpResponseRedirect(reverse('login:login'))
    
    if not Admin.objects.filter(user=user).exists():
        return HttpResponseRedirect(reverse('login:login'))
    
    form = AdminRegForm(data=request.POST or None)

    if form.is_valid():
        fName = form.cleaned_data.get('fName')
        lName = form.cleaned_data.get('lName')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        hospital = form.cleaned_data.get('hospital')
        
        accType = form.cleaned_data.get('accType')
        
        # created users are not logged in immediately, the current
        # admin user should keep access to their account

        if accType == "Admin":
            admin = Admin.objects.createAdmin(fName, lName, email, password, hospital)
            admin.user.first_name = fName
            admin.user.last_name = lName
            admin.user.save()
            admin.save()
        elif accType == "Doctor":
            doctor = Doctor.objects.createDoctor(fName, lName, email, password, hospital)
            doctor.user.first_name = fName
            doctor.user.last_name = lName
            doctor.user.save()
            doctor.save()
        elif accType == "Nurse":
            nurse = Nurse.objects.createNurse(fName, lName, email, password, hospital)
            nurse.user.first_name = fName
            nurse.user.last_name = lName
            nurse.user.save()
            nurse.save()

        logger.info("New User of type: " + accType + " Created By: "
            + Admin.objects.get(user=user).pk+ " New User Data: First Name: "
            + str(fName) + " Last Name: " + str(lName) + " Email: " + str(email))
        
        return HttpResponseRedirect(reverse('registration:admin'))
    
    return render(request, 'registration/admin.html', {'form': form})


"""
Page with warning to users about exporting medical information
"""
@login_required
def ExportPatientView(request):
    user = request.user
    
    if not Patient.objects.filter(user=user):
        return HttpResponseRedirect(reverse('login:login'))
    
    return render(request, 'registration/export.html')


"""
Compile patient info in a text file and export it
"""
@login_required
def DownloadFile(request):
    user = request.user
    
    if not Patient.objects.filter(user=user):
        return HttpResponseRedirect(reverse('login:login'))
    
    patient = Patient.objects.get(user=user)

    name = 'Name: ' + patient.fName + ' ' + patient.lName + '\n'
    email = 'Email: ' + patient.email + '\n'
    prefHospital = 'Preferred Hospital: ' + patient.prefHospital + '\n'
    weight = 'Weight: ' + str(patient.weight) + '\n'
    height = 'Height: ' + str(patient.height) + '\n'
    gender = 'Gender: ' + patient.gender + '\n'
    birthday = 'Birthday: ' + str(patient.birthday) + '\n'
    bloodtype = 'Bloodtype: ' + patient.bloodtype + '\n'
    eName = 'Emergency Contact: ' + patient.eName + ', ' + patient.ePhone

    body = name + email + prefHospital + weight + height + gender + birthday + bloodtype + eName
    
    response = HttpResponse(body, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s.txt"' % (patient.fName + '_' + patient.lName + '_info')
    
    return response
