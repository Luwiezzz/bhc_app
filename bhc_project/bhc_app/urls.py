from os import name
from django.urls import path, re_path
from django.conf.urls import static
from django.conf import settings
from django.conf.urls.static import static
from . import views

from .views  import *


app_name = 'bhc_app'

urlpatterns = [
     path('', views.index, name='index'),
     path('index/', views.index, name='index'),
     path('registration', views.registration, name='registration'),
     path('logout_user/', views.logout_user, name='logout_user'),
     

     #Patients
     path('patient_dashboard', views.patient_dashboard, name='patient_dashboard'),
     path('change_password', views.change_password, name='change_password'),
     path('change_information', views.change_information, name='change_information'),
     path('delete_account', views.delete_account, name='delete_account'),
     path('patient_doctor', views.patient_doctor, name='patient_doctor'),
     path('patient_medicine', views.patient_medicine, name='patient_medicine'),
     path('patient_news_and_update', views.patient_news_and_update, name='patient_news_and_update'),
     path('patient_set_appointment', views.patient_set_appointment, name='patient_set_appointment'),
     path('patient_set_appointment_submit', views.patient_set_appointment_submit, name='patient_set_appointment_submit'),
     path('sendalert', views.sendalert, name='sendalert'),
     




     # Admin 
     path('administrator/', views.administrator, name='administrator'),
     path('admin_homepage', views.admin_homepage, name='admin_homepage'),
     path('admin_doctor', views.admin_doctor, name='admin_doctor'),
     path('doctor_add', views.doctor_add, name='doctor_add'),
     path('doctor_edit/<int:id>', views.doctor_edit),
     path('doctor_del/<int:id>', views.doctor_del),
     
     path('admin_medicine', views.admin_medicine, name='admin_medicine'),
     path('medicine_add', views.medicine_add, name='medicine_add'),
     path('medicine_edit/<int:id>', views.medicine_edit),
     path('medicine_del/<int:id>', views.medicine_del),
     

     path('admin_appointment', views.admin_appointment, name='admin_appointment'),

     path('admin_patients', views.admin_patients, name='admin_patients'),
     path('admin_patient_history/<int:id>', views.admin_patient_history),
     path('admin_history', views.admin_history, name='admin_history'),

     path('admin_news_and_update', views.admin_news_and_update, name='admin_news_and_update'),
     path('news_add', views.news_add, name='news_add'),

     path('admin_staff', views.admin_staff, name='admin_staff'),
     path('staff_update', views.staff_update, name='staff_update'),



     
]