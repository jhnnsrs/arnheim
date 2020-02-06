import os
import sys

import django


def setup():
    sys.path.insert(0, '/code/')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "multichat.settings")
    django.setup()