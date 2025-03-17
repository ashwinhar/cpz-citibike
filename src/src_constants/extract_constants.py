"""Constants for Extract portion of ETL"""

import os

CITIBIKE_URL_PREFIX = "https://s3.amazonaws.com/tripdata/"
CITIBIKE_URL = CITIBIKE_URL_PREFIX + "index.html"
PARENT_DIR = os.path.abspath("/Users/ashwin/Desktop/cpz_citibike/")
RAW_DATA_FOLDER = os.path.join(PARENT_DIR, "data/raw_citibike_data")
# TODO: Change this to a relative path
RE_PATTERN = (
    r"https://s3\.amazonaws\.com/tripdata/\d{4,6}-citibike-tripdata(?:\.csv)?\.zip"
)
RE_PATTERN_PREFIX_BOUND = 34
YEAR_FLOOR = 2020
