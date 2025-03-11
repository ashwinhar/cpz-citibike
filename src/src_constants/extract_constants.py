"""Constants for Extract portion of ETL"""

import os

CITIBIKE_URL_PREFIX = "https://s3.amazonaws.com/tripdata/"
CITIBIKE_URL = CITIBIKE_URL_PREFIX + "index.html"
RAW_DATA_FOLDER = os.path.join(os.path.abspath("../data"), "raw_citibike_data")
RE_PATTERN = (
    r"https://s3\.amazonaws\.com/tripdata/\d{4,6}-citibike-tripdata(?:\.csv)?\.zip"
)
YEAR_FLOOR = 2020
