from django.db import models
from datetime import datetime

from registration.models import *

import logging

logger = logging.getLogger('system')

class AppointmentManager( models.Manager ):
    def scheduleAppointment( self, a_doctor, a_patient, a_title, a_description, a_date, a_starttime, a_endtime ):
        appointment = self.create( 
            a_doctor=a_doctor,
            a_patient=a_patient,
            a_title=a_title,
            a_description=a_description,
            a_date=a_date,
            a_starttime=a_starttime,
            a_endtime=a_endtime,
        )
        logger.info( "New Appointment: " + str(appointment) )
        return appointment
    

class Appointment( models.Model ):
    a_doctor      = models.ForeignKey( Doctor, related_name='a_doctor', default=None )
    a_patient     = models.ForeignKey( Patient, related_name='a_patient', default=None )
    a_title       = models.CharField( 'Title', max_length=200 )
    a_description = models.CharField( 'Description', max_length=1000 )
    a_date        = models.DateField( 'date' )
    a_starttime   = models.TimeField( 'start time' )
    a_endtime     = models.TimeField( 'end time' )

    objects = AppointmentManager()

    def __str__(self):
        display =   self.a_doctor.fName + ' ' + self.a_doctor.lName + \
                    " has an appointment with " + \
                    self.a_patient.fName + ' ' + self.a_patient.lName + \
                    " at " + self.a_starttime.strftime('%I:%M %p') + " on " + \
                    self.a_date.strftime('%B %d, %Y')

        return display

    def update(self, title, description, date, start, end):
        logger.info( "Edit Appointment: " + str(self) )

        self.a_title = title
        self.a_description = description
        self.a_date = date
        self.a_starttime = start
        self.a_endtime = end
        self.save()

    def remove( self ):
        logger.info( "Deleted Appointment: " + str(self) )

        self.delete()
