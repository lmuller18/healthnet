from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from registration.models import *
from .forms import *

def index(request):
    user = request.user
    
    # logged in users should not see the login page
    
    #if (user is not None) and (not user.is_anonymous()):
        #if Admin.objects.filter(user=user).exists():
        #    return HttpResponseRedirect('/registration/admin')
        #return HttpResponseRedirect('/dashboard/')
    
    form = LoginForm(data=request.POST or None)
    
    try:
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(username=email, password=password)
        
            if user is None:
                return render(request, 'login/index.html', {'form': form})
         
            login(request, user)
        
            #if Admin.objects.filter(user=user).exists():
            #    return HttpResponseRedirect('/registration/admin')
            
            return HttpResponseRedirect('/dashboard/')

    except Exception:
        return render(request, 'login/index.html', {'form': form})
    
    return render(request, 'login/index.html', {'form': form})

def LoginView(request):
    user = request.user
    
    # logged in users should not see the login page
    
    if (user is not None) and (not user.is_anonymous()):
        #if Admin.objects.filter(user=user).exists():
        #    return HttpResponseRedirect('/registration/admin')
        return HttpResponseRedirect('/dashboard/')
    
    form = LoginForm(data=request.POST or None)
    
    try:
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(username=email, password=password)
        
            if user is None:
                return render(request, 'login/index.html', {'form': form})
        
            login(request, user)
        
            #if Admin.objects.filter(user=user).exists():
            #    return HttpResponseRedirect('/registration/admin')
            
            return HttpResponseRedirect('/dashboard/')

    except Exception:
        return render(request, 'login/login.html', {'form': form})
    
    return render(request, 'login/login.html', {'form': form})