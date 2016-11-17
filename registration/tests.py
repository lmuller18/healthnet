from django.test import TestCase
from django.contrib.auth import authenticate
from .models import Patient, Nurse, Admin, Doctor

from .forms import *

def create_patient( fName, lName, email, password ):
    patient = Patient.objects.createPatient(
        fName=fName,
        lName=lName,
        email=email,
        password=password,
    )
    return patient

def create_admin( fName, lName, email, password ):
    admin = Admin.objects.createAdmin(
        fName=fName,
        lName=lName,
        email=email,
        password=password,
        hospital='Rochester General Hospital',
    )
    return admin

def create_doctor( fName, lName, email, password ):
    doctor = Doctor.objects.createDoctor(
        fName=fName,
        lName=lName,
        email=email,
        password=password,
        hospital='Rochester General Hospital',
    )
    return doctor

def create_nurse( fName, lName, email, password ):
    nurse = Nurse.objects.createNurse(
        fName=fName,
        lName=lName,
        email=email,
        password=password,
        hospital='Rochester General Hospital',
    )
    return nurse


class UserCreationTestCase( TestCase ):

    def setUp( self ):
        patient = create_patient( "John", "Doe", "test1@example.com", "password" )
        admin = create_admin( "This", "Person", "test2@example.com", "password" )
        doctor = create_doctor( "Another", "One", "test3@example.com", "password" )
        nurse = create_nurse( "Johnny", "Doe", "test4@example.com", "password" )

    def test_can_user_login( self ):
        user = authenticate(username="test1@example.com", password="password")
        
        self.assertEqual( user.username, "test1@example.com" )
        self.assertEqual( user.email, "test1@example.com" )
        
    def test_can_patient_be_made( self ):
        user = authenticate(username="test1@example.com", password="password")
        
        patient = Patient.objects.get(user=user)

        self.assertEqual( patient.fName, "John" )
        self.assertEqual( patient.lName, "Doe" )
        self.assertEqual( patient.email, "test1@example.com" )
    
    def test_can_admin_be_made( self ):
        user = authenticate(username="test2@example.com", password="password")
        
        admin = Admin.objects.get(user=user)

        self.assertEqual( admin.fName, "This" )
        self.assertEqual( admin.lName, "Person" )
        self.assertEqual( admin.email, "test2@example.com" )
    
    def test_can_doctor_be_made( self ):
        user = authenticate(username="test3@example.com", password="password")
        
        doctor = Doctor.objects.get(user=user)

        self.assertEqual( doctor.fName, "Another" )
        self.assertEqual( doctor.lName, "One" )
        self.assertEqual( doctor.email, "test3@example.com" )
    
    def test_can_nurse_be_made( self ):
        user = authenticate(username="test4@example.com", password="password")
        
        nurse = Nurse.objects.get(user=user)

        self.assertEqual( nurse.fName, "Johnny" )
        self.assertEqual( nurse.lName, "Doe" )
        self.assertEqual( nurse.email, "test4@example.com" )


class PatientRegFormTestCase( TestCase ):
    
    def test_patientreg_form_init( self ):
        try:
            PatientRegForm()
        except Exception:
            self.fail("PatientRegForm() initialization unexpectedly raised Exception.")

    def test_patientreg_form_valid_data( self ):
        form = PatientRegForm({
            'fName': 'Joe',
            'lName': 'Man',
            'email': 'test@email.com',
            'password': 'password',
        })

        self.assertTrue( form.is_valid() )

    def test_patientreg_form_invalid_data( self ):
        form = PatientRegForm({
            'fName': '',
            'email': '',
        })

        self.assertFalse( form.is_valid() )

    def test_patientreg_form_blank_data( self ):
        form = PatientRegForm({})

        self.assertFalse( form.is_valid() )
        
        self.assertEqual(form.errors, {
            'fName': ['This field is required.'],
            'lName': ['This field is required.'],
            'email': ['This field is required.'],
            'password': ['This field is required.'],
        })


class PatientProfileFormTestCase( TestCase ):
    
    def test_patientprofile_form_init( self ):
        try:
            PatientProfileForm()
        except Exception:
            self.fail("PatientProfileForm() initialization unexpectedly raised Exception.")

    def test_patientprofile_form_valid_data( self ):
        form = PatientProfileForm({
            'fName': 'Jim',
            'lName': 'H',
            'email': 'name@cs.rit.edu',
            'hospital': 'Rochester General Hospital',
            'height': '10',
            'weight': '10',
            'gender': 'Male',
            'birthday': '1990-01-01',
            'bloodtype': 'A',
            'eName': 'Jim H',
            'ePhone': '555-867-5309',
        })
        
        self.assertTrue( form.is_valid() )

    def test_patientprofile_form_invalid_data( self ):
        form = PatientProfileForm({
            'fName': '',
            'lName': '',
            'email': '',
            'hospital': 'Null',
            'weight': '',
            'height': '',
            'gender': 'no',
            'birthday': '19',
            'bloodtype': 'Z',
            'eName': '',
        })

        self.assertFalse( form.is_valid() )

    def test_patientprofile_form_blank_data( self ):
        form = PatientProfileForm({})

        self.assertFalse( form.is_valid() )

        self.assertEqual(form.errors, {
            'hospital': ['This field is required.'],
            'height': ['This field is required.'],
            'weight': ['This field is required.'],
            'gender': ['This field is required.'],
            'birthday': ['This field is required.'],
            'bloodtype': ['This field is required.'],
            'eName': ['This field is required.'],
            'ePhone': ['This field is required.'],
        })


class AdminRegFormTestCase( TestCase ):
    
    def test_adminreg_form_init( self ):
        try:
            AdminRegForm()
        except Exception:
            self.fail("AdminRegForm() initialization unexpectedly raised Exception.")

    def test_adminreg_form_valid_data( self ):
        form = AdminRegForm({
            'accType': 'Doctor',
            'fName': 'Joe',
            'lName': 'Man',
            'email': 'testAdmin@email.com',
            'password': 'password',
            'hospital': 'Rochester General Hospital',
        })

        self.assertTrue( form.is_valid() )

    def test_adminreg_form_invalid_data( self ):
        form = AdminRegForm({
            'accType': 'Janitor',
            'fName': 'Dr. Jan',
            'lName': 'Itor',
            'hospital': 'Unknown',
        })

        self.assertFalse( form.is_valid() )

    def test_adminreg_form_blank_data( self ):
        form = AdminRegForm({})

        self.assertFalse( form.is_valid() )
        
        self.assertEqual(form.errors, {
            'accType': ['This field is required.'],
            'fName': ['This field is required.'],
            'lName': ['This field is required.'],
            'email': ['This field is required.'],
            'password': ['This field is required.'],
            'hospital': ['This field is required.'],
        })