from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from messaging.models import *
from .models import *
from .forms import *

import logging
from registration.models import *
logger = logging.getLogger('system')

@login_required
def ListView(request):
    user = request.user
    user_type = None
    canEdit = None
    isNurse = None
    if Doctor.objects.filter(user=user).exists():
        doctor = Doctor.objects.get(user=user)
        list = Result.objects.filter(t_doctor=doctor).order_by('-t_created')
        user_type = doctor
        canEdit = True
    elif Patient.objects.filter(user=user).exists():
        patient = Patient.objects.get(user=user)
        list = Result.objects.filter(t_patient=patient).order_by('-t_created')
    elif Nurse.objects.filter(user=user).exists():
        nurse = Nurse.objects.get(user=user)
        test_list = Result.objects.all().order_by('-t_created')
        list = []
        for t in test_list:
            if t.t_patient.currHospital == nurse.hospital:
                list.append(t)
        isNurse = True
    else:
        return HttpResponseRedirect('/login/')
    return render(request, 'testResult/index.html', {
        'result_list': list,
        'doctor': user_type,
        'canEdit': canEdit,
        'isNurse': isNurse,
    })

@login_required
def Create_Result(request):
    user = request.user
    if not Doctor.objects.filter(user=user).exists():
        return HttpResponseRedirect('/login/')
    doctor_user = Doctor.objects.get(user=user)
    list = Result.objects.filter(t_doctor=doctor_user).filter(t_created__lte=timezone.now()).order_by('-t_created')
    form = TestResultForm(request.POST or None, initial={
        't_doctor': doctor_user.fName + ' ' + doctor_user.lName,

    })
    if form.is_valid():
        t_doctor = Doctor.objects.get(user=request.user)
        t_patient = Patient.objects.get(email=form.cleaned_data.get('t_patient'))
        t_testname = form.cleaned_data.get('t_testname')
        t_result = form.cleaned_data.get('t_result')

        logger.info("New Result: " + " " + str(t_doctor) + " " + str(t_patient) + " " +
                    str(t_result))

        t = Result.objects.createResult(t_doctor, t_patient, t_result)
        t.t_testname = t_testname
        t.save()

        recipient = User.objects.get(email=t_patient)
        message = Message.objects.createMessage(user, recipient, "New Result Released",
                                                "You have a new available test result. ")
        message.link = "/testResult/" + (str(t.id) + "/view/")
        message.save()

        return HttpResponseRedirect('/testResult')

    return render(request, 'testResult/index.html', {
        'newForm': form,
        'doctor': doctor_user,
        'result_list': list
    })


def View_Result(request, t_id):
    user = request.user
    user_type = None
    canEdit = None
    isNurse = None
    if Result.objects.filter(id=t_id).exists():
        result = Result.objects.get(id=t_id)
        if Patient.objects.filter(user=user).exists():
            patient = Patient.objects.get(user=user)
            list = Result.objects.filter(t_patient=patient).filter(t_created__lte=timezone.now()).order_by('-t_created')
            if not Result.objects.filter(t_patient=patient, id=t_id).exists():
                return HttpResponseRedirect('/testResult/')
            user_type = None
        elif Doctor.objects.filter(user=user).exists():
            doctor = Doctor.objects.get(user=user)
            list = Result.objects.filter(t_doctor=doctor).filter(t_created__lte=timezone.now()).order_by('-t_created')
            if not Result.objects.filter(t_doctor=doctor, id=t_id):
                return HttpResponseRedirect('/testResult')
            user_type = doctor
            if Result.objects.filter(id=t_id, t_doctor=doctor).exists():
                canEdit = True
        elif Nurse.objects.filter(user=user).exists():
            nurse = Nurse.objects.get(user=user)
            if result.t_patient.currHospital != nurse.hospital:
                return HttpResponseRedirect('/testResult')
            list = []
            for t in Result.objects.all():
                if t.t_patient.currHospital == nurse.hospital:
                    list.append(t)
            isNurse = True
        else:
            return HttpResponseRedirect('/login/')

        return render(request, 'testResult/index.html', {
            'view': result,
            'result_list': list,
            'doctor': user_type,
            'canEdit': canEdit,
            'isNures': isNurse,
        })
    else:
        return HttpResponseRedirect('/testResult/')

@login_required()
def Edit_Result(request, t_id):
    user = request.user
    if not Doctor.objects.filter(user=user).exists():
        return HttpResponseRedirect('/login/')
    doctor_user = Doctor.objects.get(user=user)

    list = Result.objects.filter(t_doctor=doctor_user).filter(t_created__lte=timezone.now()).order_by('-t_created')

    if Result.objects.filter(id=t_id, t_doctor=doctor_user).exists():
        result = Result.objects.get(id=t_id, t_doctor=doctor_user)
        form = EditForm(request.POST or None, initial={
            't_doctor': result.t_doctor,
            't_patient': result.t_patient,
            't_testname': result.t_testname,
            't_result': result.t_result,
            't_created': result.t_created,
        })
        if form.is_valid():
            t_result = form.cleaned_data.get('t_result')
            t_testname = form.cleaned_data.get('t_testname')

            result.t_result = t_result
            result.t_testname = t_testname
            result.save()
            logger.info("Edited Result: " + " " + str(result.t_doctor) + " " + str(result.t_patient) + " " +
                        str(result.t_result))
            recipient = User.objects.get(email=result.t_patient.email)
            message = Message.objects.createMessage(user, recipient, "RE: Your " + result.t_testname + "Test",
                                                    "Your Test Has Been Edited")
            message.link = "/testResult/" + (str(result.id) + "/view/")
            message.save()


            return HttpResponseRedirect('/testResult/')
        return render(request, 'testResult/index.html', {
            'editForm': form,
            'result': result,
            'doctor': doctor_user,
            'patient': result.t_patient,
            'created': result.t_created,
            'result_list': list,
        })
    else:
        return HttpResponseRedirect('/testResult/')


@login_required()
def Delete_Result(request, t_id):
    user = request.user
    if not Doctor.objects.filter(user=user).exists():
        return HttpResponseRedirect('/testResult/')

    doctor = Doctor.objects.get(user=user)

    if Result.objects.filter(id=t_id).exists():
        t = Result.objects.get(id=t_id)
        message = Message.objects.createMessage(user, User.objects.get(email=t.t_patient.email), "RE: Your " + t.t_testname + " Test",
                                                "Your Test Result Has Been Deleted")
        message.save()
        t.delete()
        list = Result.objects.filter(t_doctor=doctor).filter(t_created__lte=timezone.now()).order_by('-t_created')
        return render(request, 'testResult/index.html', {
            't': t,
            'doctor': doctor,
            'result_list': list
        })
    return HttpResponseRedirect('/testResult/')

@login_required
def DownloadFile(request):
    user = request.user

    if not Patient.objects.filter(user=user):
        return HttpResponseRedirect(reverse('login:login'))

    patient = Patient.objects.get(user=user)
    result = Result.objects.get(t_patient=patient)
    name = 'Name: ' + result.t_patient.fName + ' ' + result.t_patient.lName + '\n'
    result = 'Result: ' + result.t_result + '\n'
    created = 'Created: ' + result.t_created + '\n'
    body = name + result + created

    response = HttpResponse(body, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s.txt"' % (patient.fName + '_' + patient.lName + '_info')

    return response