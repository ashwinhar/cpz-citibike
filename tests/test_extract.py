import pytest
from src_components.data_extraction.extract import find_files_of_interest


@pytest.fixture
def sample_zip_links():
    return [
        "https://example.com/202101-citibike-tripdata.zip",
        "https://example.com/202102-citibike-tripdata.zip",
        "https://example.com/202001-citibike-tripdata.zip",
        "https://example.com/201912-citibike-tripdata.zip",
        "https://example.com/invalidfile.txt",
    ]


def test_find_files_of_interest(sample_zip_links):
    re_pattern = r"https://example\.com/\d{6}-citibike-tripdata\.zip"
    year_floor = 2020

    expected_files = [
        "202101-citibike-tripdata.zip",
        "202102-citibike-tripdata.zip",
        "202001-citibike-tripdata.zip",
    ]

    result = find_files_of_interest(sample_zip_links, re_pattern, year_floor)
    assert result == expected_files


def test_find_files_of_interest_with_higher_year_floor(sample_zip_links):
    re_pattern = r"https://example\.com/\d{6}-citibike-tripdata\.zip"
    year_floor = 2021

    expected_files = [
        "202101-citibike-tripdata.zip",
        "202102-citibike-tripdata.zip",
    ]

    result = find_files_of_interest(sample_zip_links, re_pattern, year_floor)
    assert result == expected_files


def test_find_files_of_interest_with_no_matching_files(sample_zip_links):
    re_pattern = r"https://example\.com/\d{6}-citibike-tripdata\.zip"
    year_floor = 2022

    expected_files = []

    result = find_files_of_interest(sample_zip_links, re_pattern, year_floor)
    assert result == expected_files


def test_find_files_of_interest_with_invalid_pattern(sample_zip_links):
    re_pattern = r"https://example\.com/\d{6}-invalid-pattern\.zip"
    year_floor = 2020

    expected_files = []

    result = find_files_of_interest(sample_zip_links, re_pattern, year_floor)
    assert result == expected_files
