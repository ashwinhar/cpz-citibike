"""Tests for src.src_components.data_extraction.extract.py"""

from src_components.data_extraction.extract import (
    find_files_of_interest,
    get_existing_citibike_files,
)


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


def test_get_existing_citibike_files_with_existing_files(tmp_path):
    """
    Test get_existing_citibike_files with existing .zip files in the folder
    """
    # Create temporary files
    file1 = tmp_path / "202101-citibike-tripdata.zip"
    file2 = tmp_path / "202102-citibike-tripdata.zip"
    file1.touch()
    file2.touch()

    expected_files = ["202101-citibike-tripdata.zip", "202102-citibike-tripdata.zip"]

    result = get_existing_citibike_files(folder_path=tmp_path)

    assert sorted(result) == sorted(expected_files)


def test_get_existing_citibike_files_with_no_files(tmp_path):
    """
    Test get_existing_citibike_files with no .zip files in the folder
    """
    expected_files = []

    result = get_existing_citibike_files(folder_path=tmp_path)

    assert result == expected_files


def test_get_existing_citibike_files_with_non_zip_files(tmp_path):
    """
    Test get_existing_citibike_files with non .zip files in the folder
    """
    # Create temporary files
    file1 = tmp_path / "202101-citibike-tripdata.txt"
    file2 = tmp_path / "202102-citibike-tripdata.csv"
    file1.touch()
    file2.touch()

    expected_files = []

    result = get_existing_citibike_files(folder_path=tmp_path)

    assert result == expected_files


def test_get_existing_citibike_files_with_mixed_files(tmp_path):
    """
    Test get_existing_citibike_files with mixed .zip and non .zip files in the folder
    """
    # Create temporary files
    file1 = tmp_path / "202101-citibike-tripdata.zip"
    file2 = tmp_path / "202102-citibike-tripdata.txt"
    file1.touch()
    file2.touch()

    expected_files = ["202101-citibike-tripdata.zip"]

    result = get_existing_citibike_files(folder_path=tmp_path)

    assert result == expected_files
