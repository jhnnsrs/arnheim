FROM jupyter/scipy-notebook

USER root

RUN apt-get update \
  && apt-get install -yq --no-install-recommends graphviz git libpq-dev python-dev\
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER $NB_USER

ADD requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt

RUN conda install --yes \
    -c conda-forge \
    python-blosc \
    cytoolz \
    dask==2.9.2\
    lz4 \
    zarr \
    nomkl \
    numpy==1.17.3 \
    scipy==1.4.1 \
    pandas==0.25.2 \
    ipywidgets \
    nodejs \
    ipyvolume \
    dask-labextension==1.0.3 \
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

ADD .config/dask /config/.config/dask
ADD .jupyter/jupyter_notebook_config.py /config/.jupyter/jupyter_notebook_config.py



ENV PYTHONPATH="$PYTHONPATH:/code"
ENV DJANGO_SETTINGS_MODULE="mandal.settings"
WORKDIR /config
