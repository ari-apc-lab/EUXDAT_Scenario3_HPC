FROM conda/miniconda3

RUN conda update conda \
 && conda install -c conda-forge -y \
    pillow geojson \
    mpi4py \
   # gdal==2.4.1 \
 && conda install -c esri netcdf4 \
    #jinja2 \
    #psycopg2 \cp 
 && conda clean -tipsy

RUN mkdir /frostdates
RUN mkdir /frostdates/data
RUN mkdir /frostdates/export

COPY python_code /opt/scripts
WORKDIR /opt/scripts

RUN chmod +x frostdates  
CMD mpirun -np 2 ./frostdates
#CMD python3 frostdates.py
