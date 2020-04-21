import os
import logging

DAY_IN_ROW = 1 
START_HOUR_DAY = 0 
END_HOUR_DAY = 23
FROST_DEGREE = 0
START_YEAR = 2016
END_YEAR = 2018
PROBABILITY = 10

EXPORT_FOLDER = "/zhome/academic/HLRS/eur/xeupmara/sc3_agroclimatic/frostdates/cloudify_integration/export" 
DATA_FOLDER = "/zhome/academic/HLRS/eur/xeupmara/sc3_agroclimatic/frostdates/cloudify_integration/data" 

START_LON = 12.555 
START_LAT = 49.67 
END_LON = 12.61
END_LAT = 49.801 

#INPUT_LOGLEVEL = DEBUG

process_id = "test_frostdatelatlon"

#def setup_logger(logger_name, log_file, level=INPUT_LOGLEVEL):
def setup_logger(logger_name, log_file):
  """Function setup as many loggers as needed"""

  l = logging.getLogger(logger_name)
  formatter = logging.Formatter('%(asctime)s  [%(levelname)s] - %(message)s')
  fileHandler = logging.FileHandler(log_file, mode='a')
  fileHandler.setFormatter(formatter)
  streamHandler = logging.StreamHandler()
  streamHandler.setFormatter(formatter)

  l.setLevel(logging.DEBUG)
  #l.setLevel(level)
  l.addHandler(fileHandler)
  l.addHandler(streamHandler)

