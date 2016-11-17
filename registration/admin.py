from django.contrib import admin
from .models import Patient, Doctor, Nurse, Admin

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Admin)