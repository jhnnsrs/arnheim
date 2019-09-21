FROM jupyter/scipy-notebook

RUN conda install --quiet --yes \
    'mlflow=1.0.0' \
    'psycopg2' \
    'django' \
    'django-cors-headers' \
    'django-crispy-forms' \
    'django-filter' \
    'django-pandas' \
    'django-taggit'\
    'djangorestframework' \
    'django-extensions' \
    'django-mptt'



USER root

RUN mkdir -p /code
RUN mkdir -p /files
RUN mkdir -p /media
RUN mkdir -p /config
RUN mkdir -p /notebooks
RUN mkdir -p /tmp
ADD . /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt
# install neuron
ENV PYTHONPATH="$PYTHONPATH:/code"
ENV DJANGO_SETTINGS_MODULE="mandal.settings"
WORKDIR /config
