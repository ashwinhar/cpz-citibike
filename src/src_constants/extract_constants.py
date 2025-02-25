"""Constants for Extract portion of ETL"""

import os

CITIBIKE_URL_PREFIX = "https://s3.amazonaws.com/tripdata/"
RAW_DATA_FOLDER = os.path.join(os.path.abspath("../data"), "raw_citibike_data")
RE_PATTERN = (
    "https://s3\.amazonaws\.com/tripdata/\d{4,6}-citibike-tripdata(?:\.csv)?\.zip"
)
YEAR_FLOOR = 2020
CITIBIKE_URL = CITIBIKE_URL_PREFIX + "index.html"
