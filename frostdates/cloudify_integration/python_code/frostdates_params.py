import os
import logging

DAY_IN_ROW = 1 
START_HOUR_DAY = 0 
END_HOUR_DAY = 23
FROST_DEGREE = 0
START_YEAR = 2016
#START_YEAR = 2016
END_YEAR = 2019
PROBABILITY = 10


path=os.path.abspath(__file__ + "/../../")

EXPORT_FOLDER =path+ "/export"
DATA_FOLDER = path + "/data"


#1890PAIRS
#START_LON = 12.0
#START_LAT = 48.5
#END_LON = 18.79999924
#END_LAT = 51.0

#4 PAIRS
START_LON = 12.0
START_LAT = 48.5
END_LON = 12.10000038
END_LAT = 48.59999847


#END_LAT = 49.801 

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

