"""
apps.py

Django application configuration for the Campaign Analytics app.

Defines the AppConfig subclass used by Django to register this app and
to apply default settings such as the type of primary key field.
"""
from django.apps import AppConfig


class ProjectConfig(AppConfig):
    """
    AppConfig for the 'project' Django application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project'
