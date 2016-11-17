from django.test import TestCase
from datetime import date, datetime
import time

from .models import Appointment, AppointmentManager
from registration.models import Patient, Doctor

from .forms import AppointmentForm

def create_patient( fName, lName, email, password ):
    patient = Patient.objects.createPatient(
        fName=fName,
        lName=lName,
        email=email,
        password=password,
    )
    return patient
    
def create_doctor( fName, lName, email, password ):
    doctor = Doctor.objects.createDoctor(
        fName=fName,
        lName=lName,
        email=email,
        password=password,
        hospital='Rochester General Hospital'
    )
    return doctor

def create_appointment( doctor, patient, title, description, date, starttime, endtime ):
    appointment = Appointment.objects.scheduleAppointment(
        a_doctor=doctor,
        a_patient=patient,
        a_title=title,
        a_description=description,
        a_date=date,
        a_starttime=starttime,
        a_endtime=endtime,
    )
    return appointment

class AppointmentIndexTestCase( TestCase ):

    def setUp( self ):
        self.date = datetime.now().strftime('%Y-%m-%d')
        self.time = datetime.now().strftime('%H:%M')
        self.patient = create_patient( "Patient", "Marissa", "patient@marissa.com", "password123" )
        self.doctor = create_doctor( "Doctor", "Stevens", "doctor@lewis.com", "password123" )
        patient = create_patient( "John", "Doe", "test1@example.com", "password" )
        doctor = create_doctor( "Doctor", "Lewis", "test2@example.com", "password" )
        create_appointment( doctor, patient, "Eating Bacon", "Stuff about food.", self.date, self.time, self.time )

    def test_can_appointment_be_made( self ):
        appointment = Appointment.objects.get(a_title="Eating Bacon")

        self.assertEqual( appointment.a_doctor.fName, "Doctor" )
        self.assertEqual( appointment.a_doctor.lName, "Lewis" )
        self.assertEqual( appointment.a_patient.fName, "John" )
        self.assertEqual( appointment.a_patient.lName, "Doe" )
        self.assertEqual( appointment.a_title, "Eating Bacon" )
        self.assertEqual( appointment.a_description, "Stuff about food." )
        self.assertEqual( appointment.a_date.strftime('%Y-%m-%d'), self.date )
        self.assertEqual( appointment.a_starttime.strftime('%H:%M'), self.time )
        self.assertEqual( appointment.a_endtime.strftime('%H:%M'), self.time )

    def test_appointment_form_init( self ):
        try:
            AppointmentForm()
        except Exception:
            self.fail("AppointmentForm() initialization unexpectedly raised Exception.")

    def test_appointment_form_init_with_none( self ):
        try:
            AppointmentForm( None )
        except Exception:
            self.fail("AppointmentForm() initialization unexpectedly raised Exception.")

    def test_appointment_form_valid_data( self ):
        form = AppointmentForm( {
            'a_doctor': "Doctor Stevens",
            'a_patient': "Patient Marissa",
            'a_title': "Wrist Transplant",
            'a_description': "Weird wrist problem.",
            'a_date': self.date,
            'a_starttime': self.time,
            'a_endtime': self.time,
        })

        self.assertTrue( form.is_valid() )

    def test_appointment_form_invalid_data( self ):
        form = AppointmentForm( {
            'a_doctor': "Doctor Stevens",
            'a_patient': "Patient Marissa",
            'a_title': "Wrist Transplant",
            'a_description': "Weird wrist problem.",
            'a_date': "Pineapples",
            'a_starttime': "Rainbows",
            'a_endtime': "Glass Cups",
        })

        self.assertFalse( form.is_valid() )

    def test_appointment_form_blank_data( self ):
        form = AppointmentForm( {} )

        self.assertFalse( form.is_valid() )
        
        self.assertEqual(form.errors, {
            'a_title': ['This field is required.'],
            'a_description': ['This field is required.'],
            'a_date': ['This field is required.'],
            'a_starttime': ['This field is required.'],
            'a_endtime': ['This field is required.'],
        })        

    def test_appointment_form_long_valid_doctor( self ):
        form = AppointmentForm( {
            'a_doctor': 'd' * 200,
            'a_patient': "Patient Marissa",
            'a_title': "Wrist Transplant",
            'a_description': "Weird wrist problem.",
            'a_date': self.date,
            'a_starttime': self.time,
            'a_endtime': self.time,
        })

        self.assertTrue( form.is_valid() )

    def test_appointment_form_long_invalid_doctor( self ):
        form = AppointmentForm( {
            'a_doctor': 'd' * 201,
            'a_patient': "Patient Marissa",
            'a_title': "Wrist Transplant",
            'a_description': "Weird wrist problem.",
            'a_date': self.date,
            'a_starttime': self.time,
            'a_endtime': self.time,
        })

        self.assertFalse( form.is_valid() )

    def test_appointment_form_long_valid_patient( self ):
        form = AppointmentForm( {
            'a_doctor': "Doctor Stevens",
            'a_patient': 'p' * 200,
            'a_title': "Wrist Transplant",
            'a_description': "Weird wrist problem.",
            'a_date': self.date,
            'a_starttime': self.time,
            'a_endtime': self.time,
        })

        self.assertTrue( form.is_valid() )

    def test_appointment_form_long_invalid_patient( self ):
        form = AppointmentForm( {
            'a_doctor': "Doctor Stevens",
            'a_patient': 'p' * 201,
            'a_title': "Wrist Transplant",
            'a_description': "Weird wrist problem.",
            'a_date': self.date,
            'a_starttime': self.time,
            'a_endtime': self.time,
        })

        self.assertFalse( form.is_valid() )


    def test_appointment_form_invalid_date( self ):
        form = AppointmentForm( {
            'a_doctor': "Doctor Stevens",
            'a_patient': "Patient Marissa",
            'a_title': "Wrist Transplant",
            'a_description': "Weird wrist problem.",
            'a_date': "Log Cabins",
            'a_starttime': self.time,
            'a_endtime': self.time,
        })

        self.assertFalse( form.is_valid() )

    def test_appointment_form_invalid_starttime( self ):
        form = AppointmentForm( {
            'a_doctor': "Doctor Stevens",
            'a_patient': "Patient Marissa",
            'a_title': "Wrist Transplant",
            'a_description': "Weird wrist problem.",
            'a_date': self.date,
            'a_starttime': self.date,
            'a_endtime': self.time,
        })

        self.assertFalse( form.is_valid() )

    def test_appointment_form_invalid_endtime( self ):
        form = AppointmentForm( {
            'a_doctor': "Doctor Stevens",
            'a_patient': "Patient Marissa",
            'a_title': "Wrist Transplant",
            'a_description': "Weird wrist problem.",
            'a_date': self.date,
            'a_starttime': self.time,
            'a_endtime': self.date,
        })

        self.assertFalse( form.is_valid() )

    def test_appointment_form_edit( self ):
        #patient = create_patient( "Patient", "Marissa", "patient@marissa.com", "password123" )
        appointment = create_appointment( self.doctor, self.patient, "Wrist Transplant", "Weird wrist problem.", self.date, self.time, self.time )

        form = AppointmentForm( {
            'a_doctor': "Doctor Stevens",
            'a_patient': "Patient Marissa",
            'a_title': "Wrist Transplant #2",
            'a_description': "Weird wrist problem.",
            'a_date': self.date,
            'a_starttime': self.time,
            'a_endtime': self.time,
        }, initial = {
            'a_doctor': appointment.a_doctor,
            'a_patient': appointment.a_patient,
            'a_title': appointment.a_title,
            'a_description': appointment.a_description,
            'a_date': appointment.a_date,
            'a_starttime': appointment.a_starttime,
            'a_endtime': appointment.a_endtime,
        })

        self.assertTrue( form.is_valid() )

        if form.is_valid():
            appointment.a_title = form.cleaned_data.get('a_title')
            appointment.a_description = form.cleaned_data.get('a_description')
            appointment.a_date = form.cleaned_data.get('a_date')
            appointment.a_starttime = form.cleaned_data.get('a_starttime')
            appointment.a_endtime = form.cleaned_data.get('a_endtime')
            
            appointment.save()
        
        self.assertEqual( appointment.a_title, "Wrist Transplant #2" )

