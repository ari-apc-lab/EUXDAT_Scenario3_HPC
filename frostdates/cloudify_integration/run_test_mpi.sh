export dockerregistry="registry.test.euxdat.eu/euxdat"
export service="agroclimatic_zone_frostdates"
export tag="mpi"
export input_folder=$(pwd)/data
export output_folder=$(pwd)/output_test
#docker pull $dockerregistry/$service:latest
docker run -it \
  -v "$input_folder:/frostdates/data" \
  -v "$output_folder:/frostdates/export" \
  -e INPUT_LOGLEVEL=DEBUG \
  -e DAY_IN_ROW=1 \
  -e START_HOUR_DAY=0 \
  -e END_HOUR_DAY=23 \
  -e FROST_DEGREE=0 \
  -e START_YEAR=2016 \
  -e END_YEAR=2018 \
  -e PROBABILITY=10 \
  -e EXPORT_FOLDER="/frostdates/export" \
  -e DATA_FOLDER="/frostdates/data" \
  -e START_LON=12.555 \
  -e START_LAT=49.67 \
  -e END_LON=12.61\
  -e END_LAT=49.801 \
  -e PROCESS_ID="test_frostdatesparallel"\
  $dockerregistry/$service:$tag

#docker rmi -f $service
