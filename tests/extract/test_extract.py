"""Tests for src.src_components.data_extraction.extract.py"""

from unittest.mock import MagicMock, call
import zipfile
from src_components.data_extraction.extract import (
    find_files_of_interest,
    get_existing_citibike_files,
    find_all_downloadable_files,
    download_files,
    unzip_file_recursive,
)
from src_constants.extract_constants import (
    CITIBIKE_URL_PREFIX,
    RAW_DATA_FOLDER,
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


def test_find_all_downloadable_files(mock_webdriver):
    """
    Test find_all_downloadable_files with a mock webdriver
    """
    # Arrange
    mock_driver = MagicMock()
    mock_webdriver.return_value = mock_driver

    mock_element = MagicMock()
    mock_element.get_attribute.return_value = "http://example.com/file.zip"
    mock_driver.find_elements.return_value = [mock_element]

    # Act
    result = find_all_downloadable_files()

    # Assert
    assert result == ["http://example.com/file.zip"]
    mock_driver.get.assert_called_once_with(
        "https://s3.amazonaws.com/tripdata/index.html"
    )
    mock_driver.quit.assert_called_once()


def test_find_all_downloadable_files_multiple_files(mock_webdriver):
    """
    Test find_all_downloadable_files where multiple .zip files are available
    """
    # Arrange
    mock_driver = MagicMock()
    mock_webdriver.return_value = mock_driver

    mock_element1 = MagicMock()
    mock_element1.get_attribute.return_value = "http://example.com/file1.zip"
    mock_element2 = MagicMock()
    mock_element2.get_attribute.return_value = "http://example.com/file2.zip"
    mock_driver.find_elements.return_value = [mock_element1, mock_element2]

    # Act
    result = find_all_downloadable_files()

    # Assert
    assert result == ["http://example.com/file1.zip", "http://example.com/file2.zip"]
    mock_driver.get.assert_called_once_with(
        "https://s3.amazonaws.com/tripdata/index.html"
    )
    mock_driver.quit.assert_called_once()


def test_find_all_downloadable_files_no_files(mock_webdriver):
    """
    Test find_all_downloadable_files when no valid files are present
    """
    # Arrange
    mock_driver = MagicMock()
    mock_webdriver.return_value = mock_driver

    mock_driver.find_elements.return_value = []

    # Act
    result = find_all_downloadable_files()

    # Assert
    assert result == []
    mock_driver.get.assert_called_once_with(
        "https://s3.amazonaws.com/tripdata/index.html"
    )
    mock_driver.quit.assert_called_once()


def test_download_files_missing(
    mock_get_existing_citibike_files,
    mock_find_all_downloadable_files,
    mock_find_files_of_interest,
    mock_download_citibike_file,
):
    # Arrange
    mock_get_existing_citibike_files.return_value = ["existing_file.zip"]
    mock_find_all_downloadable_files.return_value = ["file1.zip", "file2.zip"]
    mock_find_files_of_interest.return_value = ["file1.zip", "file2.zip"]

    # Act
    download_files(
        data_folder=RAW_DATA_FOLDER, url="http://example.com", download_option="missing"
    )

    # Assert
    mock_download_citibike_file.assert_called_once_with(
        CITIBIKE_URL_PREFIX + "file2.zip", RAW_DATA_FOLDER + "/file2.zip"
    )


def test_download_files_specific(
    mock_get_existing_citibike_files,
    mock_find_all_downloadable_files,
    mock_find_files_of_interest,
    mock_download_citibike_file,
):
    # Arrange
    mock_get_existing_citibike_files.return_value = ["existing_file.zip"]
    mock_find_all_downloadable_files.return_value = ["file1.zip", "file2.zip"]
    mock_find_files_of_interest.return_value = ["file1.zip", "file2.zip"]

    # Act
    download_files(
        data_folder=RAW_DATA_FOLDER,
        url="http://example.com",
        download_option="specific",
        file_names=["file1.zip"],
    )

    # Assert
    mock_download_citibike_file.assert_called_once_with(
        CITIBIKE_URL_PREFIX + "file1.zip", RAW_DATA_FOLDER + "/file1.zip"
    )


def test_download_files_not_available(
    mock_get_existing_citibike_files,
    mock_find_all_downloadable_files,
    mock_find_files_of_interest,
    mock_download_citibike_file,
    capsys,
):
    # Arrange
    mock_get_existing_citibike_files.return_value = ["existing_file.zip"]
    mock_find_all_downloadable_files.return_value = ["file1.zip"]
    mock_find_files_of_interest.return_value = ["file1.zip"]

    # Act
    download_files(
        data_folder=RAW_DATA_FOLDER,
        url="http://example.com",
        download_option="specific",
        file_names=["file2.zip"],
    )

    # Assert
    captured = capsys.readouterr()
    assert "file2.zip not available for download" in captured.out
    mock_download_citibike_file.assert_not_called()


def test_download_files_already_exists(
    mock_get_existing_citibike_files,
    mock_find_all_downloadable_files,
    mock_find_files_of_interest,
    mock_download_citibike_file,
    capsys,
):
    # Arrange
    mock_get_existing_citibike_files.return_value = ["file1.zip"]
    mock_find_all_downloadable_files.return_value = ["file1.zip"]
    mock_find_files_of_interest.return_value = ["file1.zip"]

    # Act
    download_files(
        data_folder=RAW_DATA_FOLDER,
        url="http://example.com",
        download_option="specific",
        file_names=["file1.zip"],
    )

    # Assert
    captured = capsys.readouterr()
    assert "file1.zip already in" in captured.out
    mock_download_citibike_file.assert_not_called()


def test_unzip_file_recursive_success(mock_os_path, mock_os_listdir, mock_zipfile):
    """
    Test unzip_file_recursive with a valid zip file
    """
    # Arrange
    mock_os_path.isfile.return_value = False
    mock_os_path.isdir.return_value = False
    mock_os_listdir.return_value = []

    mock_zip = MagicMock()
    mock_zipfile.return_value.__enter__.return_value = mock_zip

    zip_file_path = "test.zip"
    extract_location = "test"

    # Act
    unzip_file_recursive(zip_file_path)

    # Assert
    mock_zip.extractall.assert_called_once_with(extract_location)
    mock_zipfile.assert_called_once_with(zip_file_path, "r")


def test_unzip_file_recursive_bad_zip_file(
    mock_os_path, mock_os_listdir, mock_zipfile, capsys
):
    """
    Test unzip_file_recursive with a bad zip file
    """
    # Arrange
    mock_os_path.isfile.return_value = False
    mock_os_path.isdir.return_value = False
    mock_os_listdir.return_value = []

    mock_zipfile.side_effect = zipfile.BadZipFile

    zip_file_path = "test.zip"

    # Act
    unzip_file_recursive(zip_file_path)

    # Assert
    captured = capsys.readouterr()
    assert "Error: The file is not a valid zip archive." in captured.out


def test_unzip_file_recursive_file_not_found(
    mock_os_path, mock_os_listdir, mock_zipfile, capsys
):
    """
    Test unzip_file_recursive with a zip file that doesn't exist
    """
    # Arrange
    mock_os_path.isfile.return_value = False
    mock_os_path.isdir.return_value = False
    mock_os_listdir.return_value = []

    mock_zipfile.side_effect = FileNotFoundError

    zip_file_path = "test.zip"

    # Act
    unzip_file_recursive(zip_file_path)

    # Assert
    captured = capsys.readouterr()
    assert "Error: The zip file was not found." in captured.out


def test_unzip_file_recursive_permission_error(
    mock_os_path, mock_os_listdir, mock_zipfile, capsys
):
    """
    Test unzip_file_recursive with a zip file that has permission issues
    """
    # Arrange
    mock_os_path.isfile.return_value = False
    mock_os_path.isdir.return_value = False
    mock_os_listdir.return_value = []

    mock_zipfile.side_effect = PermissionError

    zip_file_path = "test.zip"

    # Act
    unzip_file_recursive(zip_file_path)

    # Assert
    captured = capsys.readouterr()
    assert "Error: Permission denied when accessing the file." in captured.out


def test_unzip_file_recursive_nested_zip(mock_os_path, mock_os_listdir, mock_zipfile):
    # Arrange
    mock_os_path.isfile.side_effect = lambda path: path == "test/nested.zip"
    mock_os_path.isdir.side_effect = lambda path: path == "test"
    mock_os_listdir.side_effect = lambda path: ["nested.zip"] if path == "test" else []

    mock_zip = MagicMock()
    mock_zipfile.return_value.__enter__.return_value = mock_zip

    zip_file_path = "test.zip"
    extract_location = "test"
    nested_zip_path = "test/nested.zip"

    # Act
    unzip_file_recursive(zip_file_path)

    # Assert
    mock_zip.extractall.assert_called_once_with(extract_location)
    mock_zipfile.assert_has_calls(
        [call(zip_file_path, "r"), call(nested_zip_path, "r")]
    )
