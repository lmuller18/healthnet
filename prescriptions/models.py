from registration.models import *


class PrescriptionManager(models.Manager):
    def createPrescription(self, p_doctor, p_patient, p_prescription, p_expiration):
        p = self.create(p_doctor=p_doctor, p_patient=p_patient, p_prescription=p_prescription, p_expiration=p_expiration)
        return p


class Prescription(models.Model):
    p_patient = models.ForeignKey(Patient, related_name='patient', default=None)
    p_doctor = models.ForeignKey(Doctor, related_name='p_doctor', default=None)
    p_prescription = models.CharField('Medication', max_length=200)
    p_dose = models.IntegerField('Dosage', default=0)
    labels = (
        ('mg', 'mg'),
        ('cc', 'cc'),
    )
    p_units = models.CharField('units', max_length=5, choices=labels, default='mg')
    p_refills = models.IntegerField('Refills', default=0)
    p_expiration = models.DateField('expiration date')
    p_created = models.DateField('date created', default=datetime.now)

    objects = PrescriptionManager()

    def __str__(self):
        return str(self.p_dose) + self.p_units + " of " + self.p_prescription

