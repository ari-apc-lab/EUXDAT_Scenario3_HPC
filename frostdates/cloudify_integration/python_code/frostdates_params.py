import os
import logging

DAY_IN_ROW = os.getenv('DAY_IN_ROW')
START_HOUR_DAY = os.getenv('START_HOUR_DAY')
END_HOUR_DAY = os.getenv('END_HOUR_DAY')
FROST_DEGREE = os.getenv('FROST_DEGREE')
START_YEAR = os.getenv('START_YEAR')
END_YEAR = os.getenv('END_YEAR')
PROBABILITY = os.getenv('PROBABILITY')

EXPORT_FOLDER = os.getenv('EXPORT_FOLDER')
DATA_FOLDER = os.getenv('DATA_FOLDER')

START_LON = os.getenv('START_LON')
START_LAT = os.getenv('START_LAT')
END_LON = os.getenv('END_LON')
END_LAT = os.getenv('END_LAT')

INPUT_LOGLEVEL = os.getenv('INPUT_LOGLEVEL',logging.DEBUG)

process_id = os.getenv('PROCESS_ID')

def setup_logger(logger_name, log_file, level=INPUT_LOGLEVEL):
  """Function setup as many loggers as needed"""

  l = logging.getLogger(logger_name)
  formatter = logging.Formatter('%(asctime)s  [%(levelname)s] - %(message)s')
  fileHandler = logging.FileHandler(log_file, mode='a')
  fileHandler.setFormatter(formatter)
  streamHandler = logging.StreamHandler()
  streamHandler.setFormatter(formatter)

  l.setLevel(level)
  l.addHandler(fileHandler)
  l.addHandler(streamHandler)

