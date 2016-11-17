from django.db import models
from registration.models import *
from django.db import models
from datetime import datetime


class ResultManager(models.Manager):
    def createResult(self, t_doctor, t_patient, t_result):
        t = self.create(t_doctor=t_doctor, t_patient=t_patient, t_result=t_result)
        return t


class Result(models.Model):
    t_patient = models.ForeignKey(Patient, related_name='t_patient', default=None)
    t_doctor = models.ForeignKey(Doctor, related_name='t_doctor', default=None)
    t_result = models.CharField('Result', max_length=200)
    t_created = models.DateField('date created', default=datetime.now)
    t_testname = models.CharField('Test Name', max_length=100, default='')
    objects = ResultManager()

    def __str__(self):
        return self.t_result


