#!/usr/bin/env bash
python manage.py loaddata transformer
python manage.py loaddata node
python manage.py loaddata filter