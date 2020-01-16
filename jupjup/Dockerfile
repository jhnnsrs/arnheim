FROM jupyter/scipy-notebook

USER root

RUN apt-get update \
  && apt-get install -yq --no-install-recommends graphviz git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER $NB_USER

RUN conda install --quiet --yes \
    'mlflow=1.0.0' \
    'psycopg2' \
    'django<3,>=2' \
    'django-cors-headers' \
    'django-crispy-forms' \
    'django-filter' \
    'django-pandas' \
    'django-taggit'\
    'djangorestframework' \
    'django-extensions' \
    'django-mptt'

RUN conda install --yes \
    -c conda-forge \
    python-blosc \
    cytoolz \
    dask \
    lz4 \
    zarr \
    nomkl \
    numpy \
    pandas \
    ipywidgets \
    nodejs \
    ipyvolume \
    dask-labextension \
    python-graphviz \
    xarray \
    seaborn \
    && jupyter labextension install @jupyter-widgets/jupyterlab-manager dask-labextension@1.0.1 ipyvolume jupyter-threejs\
    && conda clean -tipsy \
    && jupyter lab clean \
    && jlpm cache clean \
    && npm cache clean --force \
    && find /opt/conda/ -type f,l -name '*.a' -delete \
    && find /opt/conda/ -type f,l -name '*.pyc' -delete \
    && find /opt/conda/ -type f,l -name '*.js.map' -delete \
    && find /opt/conda/lib/python*/site-packages/bokeh/server/static -type f,l -name '*.js' -not -name '*.min.js' -delete \
    && rm -rf /opt/conda/pkgs



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

ENV PYTHONPATH="$PYTHONPATH:/code"
ENV DJANGO_SETTINGS_MODULE="mandal.settings"
WORKDIR /config
