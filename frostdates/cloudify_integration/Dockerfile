FROM conda/miniconda3

RUN conda update conda \
 && conda install -c conda-forge -y \
    #pillow \
    gdal==2.4.1 \
 && conda install -c esri netcdf4 \
    #jinja2 \
    #psycopg2 \cp 
 && conda clean -tipsy

RUN mkdir /frostdates
RUN mkdir /frostdates/data
RUN mkdir /frostdates/export

ENV INPUT_FOLDER /var/data/
ENV OUTPUT_FOLDER /var/output/

COPY python_code /opt/scripts

WORKDIR /opt/scripts

CMD python3 xalkidiki.py
