import os
from celery import Celery


#setting the default  Django settings  module for  the  'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
# setting the DJANGO_SETTINGS_MODULE variable for  the Celery command-line program
app = Celery('myshop')
#creating an instance of the application with app = Celery('myshop)
app.config_from_object('django.conf:settings', namespace='CELERY')
#loading any custom  configuration from my project settings using the config_from_object() method
app.autodiscover_tasks()

