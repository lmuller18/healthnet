from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


"""
Admin account creation
"""
class AdminManager(models.Manager):
    def createAdmin(self, fName, lName, email, password, hospital):
        admin_user = User.objects.create_user(username=email, email=email, password=password)
        admin = self.create(user=admin_user, fName=fName, lName=lName, email=email, hospital=hospital)
        return admin


"""
Admin model
"""
class Admin(models.Model):
    user = models.ForeignKey(User, related_name='admin_user', default=None)
    fName = models.CharField('First Name', max_length=20, default=None)
    lName = models.CharField('Last Name', max_length=20, default=None)
    email = models.CharField('Email', primary_key=True, max_length=50, default=None)
    
    hLabels = {
        ('Rochester General Hospital', 'Rochester General Hospital'),
        ('Rochester Private Hospital', 'Rochester Private Hospital'),
        ('Cleveland Clinic', 'Cleveland Clinic'),
        ('University of Pittsburgh Medical Center', 'University of Pittsburgh Medical Center'),
        ('UCLA Medical Center', 'UCLA Medical Center')
    }
    hospital = models.CharField('Hospital', max_length=50, choices=hLabels, default='Rochester General Hospital')

    objects = AdminManager()
    
    def __str__(self):
        return self.email


"""
Doctor account creation
"""
class DoctorManager(models.Manager):
    def createDoctor(self, fName, lName, email, password, hospital):
        doctor_user = User.objects.create_user(username=email, email=email, password=password)
        doctor = self.create(user=doctor_user, fName=fName, lName=lName, email=email, hospital=hospital)
        return doctor


"""
Doctor model
"""
class Doctor(models.Model):
    user = models.ForeignKey(User, related_name='doctor_user', default=None)
    fName = models.CharField('First Name', max_length=20, default=None)
    lName = models.CharField('Last Name', max_length=20, default=None)
    email = models.CharField('Email', primary_key=True, max_length=50, default=None)
    
    hLabels = {
        ('Rochester General Hospital', 'Rochester General Hospital'),
        ('Rochester Private Hospital', 'Rochester Private Hospital'),
        ('Cleveland Clinic', 'Cleveland Clinic'),
        ('University of Pittsburgh Medical Center', 'University of Pittsburgh Medical Center'),
        ('UCLA Medical Center', 'UCLA Medical Center')
    }
    hospital = models.CharField('Hospital', max_length=50, choices=hLabels, default='Rochester General Hospital')
    
    objects = DoctorManager()
    
    def __str__(self):
        return self.email


"""
Nurse account creation
"""
class NurseManager(models.Manager):
    def createNurse(self, fName, lName, email, password, hospital):
        nurse_user = User.objects.create_user(username=email, email=email, password=password)
        nurse = self.create(user=nurse_user, fName=fName, lName=lName, email=email, hospital=hospital)
        return nurse


"""
Nurse model
"""
class Nurse(models.Model):
    user = models.ForeignKey(User, related_name='nurse_user', default=None)
    fName = models.CharField('First Name', max_length=20, default=None)
    lName = models.CharField('Last Name', max_length=20, default=None)
    email = models.CharField('Email', primary_key=True, max_length=50, default=None)
    
    hLabels = {
        ('Rochester General Hospital', 'Rochester General Hospital'),
        ('Rochester Private Hospital', 'Rochester Private Hospital'),
        ('Cleveland Clinic', 'Cleveland Clinic'),
        ('University of Pittsburgh Medical Center', 'University of Pittsburgh Medical Center'),
        ('UCLA Medical Center', 'UCLA Medical Center')
    }
    hospital = models.CharField('Hospital', max_length=50, choices=hLabels, default='Rochester General Hospital')
    
    objects = NurseManager()
    
    def __str__(self):
        return self.email


"""
Patient account creation. Unlike the other models, this only fills some of the
    patient fields. The rest have defaults that will usually be changed in
    the profile edit/creation views.
"""
class PatientManager(models.Manager):
    def createPatient(self, fName, lName, email, password):
        patient_user = User.objects.create_user(username=email, email=email, password=password)
        patient = self.create(user=patient_user, fName=fName, lName=lName, email=email)
        return patient


"""
Patient model
"""
class Patient(models.Model):
    user = models.ForeignKey(User, related_name='patient_user', default=None)
    fName = models.CharField('First Name', max_length=20, default=None)
    lName = models.CharField('Last Name', max_length=20, default=None)
    email = models.CharField('Email', primary_key=True, max_length=50, default=None)
    
    hLabels = {
        ('Rochester General Hospital', 'Rochester General Hospital'),
        ('Rochester Private Hospital', 'Rochester Private Hospital'),
        ('Cleveland Clinic', 'Cleveland Clinic'),
        ('University of Pittsburgh Medical Center', 'University of Pittsburgh Medical Center'),
        ('UCLA Medical Center', 'UCLA Medical Center')
    }
    prefHospital = models.CharField('Preferred Hospital', max_length=50, choices=hLabels, default='Rochester General Hospital')
    currHospital = models.CharField('Current Hospital', max_length=50, choices=hLabels, default='Not in hospital')
    
    #medical information
    
    gLabels = {
        ('Male', 'Male'),
        ('Female', 'Female'),
    }
    gender = models.CharField('Gender', max_length=10, choices=gLabels, default='M')
    height = models.IntegerField('Height', default=0)
    weight = models.IntegerField('Weight', default=0)
    birthday = models.DateField('Birthday', default='1990-01-01')

    bLabels = {
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    }
    bloodtype = models.CharField('Blood Type', max_length=5, choices=bLabels, default='A')
    
    # emergency contact information
    
    eName = models.CharField('Emergency Contact Name', max_length=60, default="Name")
    ePhone = models.CharField('Emergency Contact Phone Number', max_length=12, default="000-000-0000")

    objects = PatientManager()

    def __str__(self):
        return self.email