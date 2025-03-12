"""Standard fixtures for src.src_components.data_extraction tests"""

from unittest.mock import patch
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
    ) as mock_driver_manager:
        yield mock_driver_manager


@pytest.fixture
def mock_get_existing_citibike_files():
    """
    Mock get_existing_citibike_files() function from extract.py
    """
    with patch(
        "src.src_components.data_extraction.extract.get_existing_citibike_files"
    ) as mock:
        yield mock


@pytest.fixture
def mock_find_all_downloadable_files():
    """
    Mock find_all_downloadable_files() function from extract.py
    """
    with patch(
        "src.src_components.data_extraction.extract.find_all_downloadable_files"
    ) as mock:
        yield mock


@pytest.fixture
def mock_find_files_of_interest():
    """
    Mock find_files_of_interest() function from extract.py
    """
    with patch(
        "src.src_components.data_extraction.extract.find_files_of_interest"
    ) as mock:
        yield mock


@pytest.fixture
def mock_download_citibike_file():
    """
    Mock download_citibike_file() function from extract.py
    """
    with patch("src_components.data_extraction.extract.download_citibike_file") as mock:
        yield mock


@pytest.fixture
def mock_os_path():
    """
    Mock os.path()
    """
    with patch("src_components.data_extraction.extract.os.path") as mock:
        yield mock


@pytest.fixture
def mock_os_listdir():
    """
    Mock os.listdir()
    """
    with patch("src_components.data_extraction.extract.os.listdir") as mock:
        yield mock


@pytest.fixture
def mock_zipfile():
    """
    Mock zipfile.ZipFile
    """
    with patch("src_components.data_extraction.extract.zipfile.ZipFile") as mock:
        yield mock


@pytest.fixture
def mock_os_rmdir():
    with patch("src_components.data_extraction.organize.os.rmdir") as mock:
        yield mock


@pytest.fixture
def mock_shutil_move():
    with patch("src_components.data_extraction.organize.shutil.move") as mock:
        yield mock
