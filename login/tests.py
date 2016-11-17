from django.test import TestCase
from django.contrib.auth.models import User
from .forms import *

class LoginFormTestCase( TestCase ):
    
    def test_login_form_init( self ):
        try:
            LoginForm()
        except Exception:
            self.fail("LoginForm() initialization unexpectedly raised Exception.")

    def test_login_form_valid_data( self ):
        user = User.objects.create_user(username='mail@m.com', email='mail@m.com', password='pass')
        
        form = LoginForm({
            'email': 'mail@m.com',
            'password': 'pass',
        })
        
        self.assertTrue( form.is_valid() )

    def test_login_form_invalid_data( self ):
        form = LoginForm({
            'password': '',
        })

        self.assertFalse( form.is_valid() )

    def test_login_form_blank_data( self ):
        form = LoginForm({})

        self.assertFalse( form.is_valid() )

        self.assertEqual(form.errors, {
            'email': ['This field is required.'],
            'password': ['This field is required.'],
        })