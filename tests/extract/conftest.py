"""Standard fixtures for src.src_components.data_extraction tests"""

import pytest
from unittest.mock import patch


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


@pytest.fixture
def mock_webdriver():
    """
    Mock the webdriver.Chrome class. Simulates Selenium
    """
    with patch(
        "src.src_components.data_extraction.extract.webdriver.Chrome"
    ) as mock_web_driver:
        yield mock_web_driver


@pytest.fixture
def mock_chrome_service():
    """
    Mock the Service class. Simulates Selenium
    """
    with patch("src.src_components.data_extraction.extract.Service") as mock_service:
        yield mock_service


@pytest.fixture
def mock_chrome_driver_manager():
    """
    Mock the ChromeDriverManager class. Simulates Selenium
    """
    with patch(
        "src.src_components.data_extraction.extract.ChromeDriverManager"
    ) as mock_chrome_driver_manager:
        yield mock_chrome_driver_manager
