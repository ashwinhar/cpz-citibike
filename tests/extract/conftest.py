"""Standard fixtures for src.src_components.data_extraction tests"""

import pytest


@pytest.fixture(scope="function")
def sample_zip_links():
    """Generate sample zip_links"""
    return [
        "https://example.com/202101-citibike-tripdata.zip",
        "https://example.com/202102-citibike-tripdata.zip",
        "https://example.com/202001-citibike-tripdata.zip",
        "https://example.com/201912-citibike-tripdata.zip",
        "https://example.com/invalidfile.txt",
    ]


@pytest.fixture(scope="function")
def re_pattern():
    """Generate sample re_pattern and prefix_bound"""
    return {
        "re_pattern": r"https://example\.com/\d{6}-citibike-tripdata\.zip",
        "prefix_bound": 20,
    }
