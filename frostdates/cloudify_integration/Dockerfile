FROM conda/miniconda3

RUN conda update conda \
 && conda install -c conda-forge -y \
    pillow geojson \
    gdal==2.4.1 \
 && conda install -c esri netcdf4 \
    #jinja2 \
    #psycopg2 \cp 
 && conda clean -tipsy

RUN mkdir /frostdates
RUN mkdir /frostdates/data
RUN mkdir /frostdates/export

COPY python_code /opt/scripts
WORKDIR /opt/scripts

CMD python3 frostdates.py
