import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

import os, sys
import django

def setup():
    sys.path.insert(0, '/code/')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "multichat.settings")
    django.setup()