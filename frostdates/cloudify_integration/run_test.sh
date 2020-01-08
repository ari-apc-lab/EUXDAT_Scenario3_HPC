export dockerregistry="registry.test.euxdat.eu/euxdat"
export service="xalkidiki_scenario_v3"
export input_folder=$(pwd)/input_test
export output_folder=$(pwd)/output
docker pull $dockerregistry/$service:latest
docker run -it \
  --entrypoint=/bin/bash \
  -v "$input_folder:/var/data" \
  -v "$output_folder:/var/output" \
  -v "/data/euxdat-mapserver/maps:/maps" \
  -e INPUT_LOGLEVEL=DEBUG \
  -e INPUT_FIELD_PK=10 \
  -e INPUT_TIMESTAMP='2018-05-01T09:06:01.024Z' \
  -e INPUT_CONNECTION_STRING="dbname=geodbbackenddevel user=geodbdevel password=Euxdat12345 host=10.97.68.140 port=5432" \
  -e OUTPUT_RASTERFILE=zob.tif \
  -e PROCESS_ID=test_27051317 \
  $service 
#docker rmi -f $service
