"""Tests for src.src_components.data_extraction.extract.py"""

from src_components.data_extraction.extract import find_files_of_interest


def test_find_files_of_interest(sample_zip_links, re_pattern):
    """
    Test base functionality, finding specific files of interest given a year floor
    and re_pattern
    """

    year_floor = 2020

    expected_files = [
        "202101-citibike-tripdata.zip",
        "202102-citibike-tripdata.zip",
        "202001-citibike-tripdata.zip",
    ]

    result = find_files_of_interest(
        sample_zip_links,
        re_pattern.get("re_pattern"),
        re_pattern.get("prefix_bound"),
        year_floor,
    )
    assert result == expected_files


def test_find_files_of_interest_with_higher_year_floor(sample_zip_links, re_pattern):
    """
    Ensure files from a year before the year_floor are excluded
    """
    year_floor = 2021

    expected_files = [
        "202101-citibike-tripdata.zip",
        "202102-citibike-tripdata.zip",
    ]

    result = find_files_of_interest(
        sample_zip_links,
        re_pattern.get("re_pattern"),
        re_pattern.get("prefix_bound"),
        year_floor,
    )
    assert result == expected_files


def test_find_files_of_interest_with_no_matching_files(sample_zip_links, re_pattern):
    """
    Test case with no matching files
    """
    year_floor = 2022

    expected_files = []

    result = find_files_of_interest(
        sample_zip_links,
        re_pattern.get("re_pattern"),
        re_pattern.get("prefix_bound"),
        year_floor,
    )
    assert result == expected_files


def test_find_files_of_interest_with_invalid_pattern(sample_zip_links, re_pattern):
    """
    Test if re_pattern doesn't find any files
    """
    re_pattern["re_pattern"] = r"https://example\.com/\d{6}-invalid-pattern\.zip"
    year_floor = 2020

    expected_files = []

    result = find_files_of_interest(
        sample_zip_links,
        re_pattern.get("re_pattern"),
        re_pattern.get("prefix_bound"),
        year_floor,
    )
    assert result == expected_files
