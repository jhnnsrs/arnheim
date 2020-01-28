FROM continuumio/miniconda3:4.7.12

RUN conda install --yes \
    -c conda-forge \
    python-blosc \
    cytoolz \
    zarr \
    dask[complete] \
    lz4 \
    nomkl \
    numpy \
    pandas \
    tini\
    xarray \
    seaborn \
    && conda clean -tipsy \
    && find /opt/conda/ -type f,l -name '*.a' -delete \
    && find /opt/conda/ -type f,l -name '*.pyc' -delete \
    && find /opt/conda/ -type f,l -name '*.js.map' -delete \
    && find /opt/conda/lib/python*/site-packages/bokeh/server/static -type f,l -name '*.js' -not -name '*.min.js' -delete \
    && rm -rf /opt/conda/pkgs


RUN mkdir -p /tmp
RUN mkdir -p /code
ADD . /tmp
WORKDIR /tmp
RUN /opt/conda/bin/pip install -r requirements.txt

WORKDIR /code

COPY prepare.sh /usr/bin/prepare.sh

RUN mkdir /opt/app

#ENTRYPOINT ["tini", "-g", "--", "/usr/bin/prepare.sh"]