"""
WSGI config for cs412 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs412.settings")

application = get_wsgi_application()