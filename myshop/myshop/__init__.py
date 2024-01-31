#import celery in Django to ensure it's loaded  when django starts
from .celery import  app as celery_app


__all__ = ['celery_app']



