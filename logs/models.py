from django.db import models


class Log(models.Model):
    log = models.CharField('log', max_length=500)

    def __init__(self, log):
        self.log = log

    def __str__(self):
        return self.log


class Hospital_Statistic(models.Model):
    statistic = models.CharField('statistic', max_length=500)
    value = models.IntegerField('value', default=0)

    def __init__(self, statistic, value):
        self.statistic = statistic
        self.value = value

    def __str__(self):
        return 'Hospital: ' + self.statistic + ' | Number of Patients: ' + str(self.value)


class Prescription_Statistic(models.Model):
    statistic = models.CharField('statistic', max_length=500)
    value = models.IntegerField('value', default=0)
    average = models.DecimalField('average', max_digits=5, decimal_places=2, default=0)
    units = models.CharField('units', max_length=5, default='mg')

    def __init__(self, statistic, value, average, units):
        self.statistic = statistic
        self.value = value
        self.average = average
        self.units = units

    def __str__(self):
        return 'Prescription: ' + self.statistic + ' | Number of Prescriptions: ' + str(
            self.value) + ' | Average Dose: ' + str(self.average) + self.units
