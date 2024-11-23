from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from .models import Appointment
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor_name','patient_name','appointment_types', 'appointment_status','symptom','time','cancel'] # nicher function er name gula use korte hobe ekhane.
    
    def patient_name(self,obj): # name gula nijer moto kore dite parbe
        return obj.patient.user.first_name # patient er sathe user model er connection ache tai user model er kache giye tar first name ke ber kore anlam
    
    def doctor_name(self,obj):
        return obj.doctor.user.first_name
    
    def save_model(self,request, obj, form,change):
        obj.save()
        if obj.appointment_status == "Running" and obj.appointment_types == "Online":
            email_subject = "Your Online Appointment is Running"
            email_body = render_to_string('admin_email.html', {'user' : obj.patient.user, 'doctor' : obj.doctor})
            
            email = EmailMultiAlternatives(email_subject , '', to=[obj.patient.user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
    
admin.site.register(Appointment,AppointmentAdmin)