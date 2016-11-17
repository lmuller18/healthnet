from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import *
from .forms import *
from registration.models import *

import logging

logger = logging.getLogger('system')


@login_required
def MessagingView(request):
    user = request.user
    context = getContext(user)
    return render(request, 'messaging/messagingDash.html', context)


@login_required
def New_Message(request):
    user = request.user
    user_type = getUser(user)
    context = getContext(user)
    form = NewMessageForm(request.POST or None, initial={
        'sender': user_type.fName + ' ' + user_type.lName,
    })

    if form.is_valid():
        rEmail = form.cleaned_data.get('recipient')
        recipient = User.objects.get(email=rEmail)
        subject = form.cleaned_data.get('subject')
        content = form.cleaned_data.get('content')

        message = Message.objects.createMessage(user, recipient, subject, content)

        message.save()
        return HttpResponseRedirect('/messaging/')
    context['newForm'] = form
    return render(request, 'messaging/messagingDash.html', context)


@login_required
def Respond(request, parent_id):
    user = request.user
    user_type = getUser(user)

    parent = Message.objects.get(id=parent_id)
    recipient = parent.sender
    if parent.sender == user:
        recipient = parent.recipient
    r_type = getUser(recipient)
    form = RespondMessageForm(request.POST or None, initial={
        'sender': user_type.fName + ' ' + user_type.lName,
        'recipient': r_type.fName + ' ' + r_type.lName,
        'subject': "RE: " + parent.subject
    })
    if form.is_valid():
        subject = form.cleaned_data.get('subject')
        content = form.cleaned_data.get('content')

        message = Message.objects.createMessage(user, recipient, subject, content)

        message.save()

        return HttpResponseRedirect('/messaging/')
    context = getContext(user)
    context['respondForm'] = form
    return render(request, 'messaging/messagingDash.html', context)



@login_required
def View_Message(request, m_id):
    user = request.user
    if Message.objects.all().filter(Q(sender=user, id=m_id, sender_hidden=False) |
                                    Q(recipient=user, id=m_id, recipient_hidden=False)).exists():
        message = Message.objects.get(id=m_id)
        form = RespondMessageForm(request.POST or None, initial={
            'sender': message.sender,
            'recipient': message.recipient,
            'subject': message.subject,
            'content': message.content
        })
        message.read = True
        message.save()
        context = getContext(user)
        context['viewForm'] = form
        context['view'] = message
        return render(request, 'messaging/messagingDash.html', context)
    return HttpResponseRedirect('/messaging/')


@login_required
def Delete_Message(request, m_id):
    user = request.user
    if Message.objects.all().filter(Q(sender=user, id=m_id)).exists():
        message = Message.objects.get(id=m_id)
        if message.recipient_hidden:
            message.delete()
        elif message.recipient == user:
            message.delete()
        else:
            message.sender_hidden = True
            message.save()
        context = getContext(user)
        context['m'] = message
        return render(request, 'messaging/messagingDash.html', context)
    elif Message.objects.all().filter(Q(recipient=user, id=m_id)).exists():
        message = Message.objects.get(id=m_id)
        if message.sender_hidden:
            message.delete()
        elif message.sender == user:
            message.delete()
        else:
            message.recipient_hidden = True
            message.save()
        context = getContext(user)
        context['m'] = message
        return render(request, 'messaging/messagingDash.html', context)
    return HttpResponseRedirect('/login/')


def getUser(user):
    if Doctor.objects.filter(user=user).exists():
        user_type = Doctor.objects.get(user=user)
    elif Patient.objects.filter(user=user).exists():
        user_type = Patient.objects.get(user=user)
    elif Nurse.objects.filter(user=user).exists():
        user_type = Nurse.objects.get(user=user)
    elif Admin.objects.filter(user=user).exists():
        user_type = Admin.objects.get(user=user)
    else:
        return HttpResponseRedirect('/login/')
    return user_type


def getContext(user):
    message_list = Message.objects.all().filter(Q(sender=user, sender_hidden=False) |
                                                Q(recipient=user, recipient_hidden=False)).filter(
        pubdate__lte=timezone.now()).order_by('-pubdate')
    inbox = Message.objects.all().filter(Q(recipient=user, recipient_hidden=False)).filter(
        pubdate__lte=timezone.now()).order_by('-pubdate')
    sent = Message.objects.all().filter(Q(sender=user, sender_hidden=False)).filter(
        pubdate__lte=timezone.now()).order_by('-pubdate')

    context = {
        'message_list': message_list,
        'inbox': inbox,
        'sent': sent,
    }
    return context
