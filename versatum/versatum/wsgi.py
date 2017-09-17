"""
WSGI config for versatum project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.insert(0, '/var/www/versatum.org/website/versatum/')

os.environ["DJANGO_SETTINGS_MODULE"] = "versatum.settings"
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "versatum.settings")

application = get_wsgi_application()
