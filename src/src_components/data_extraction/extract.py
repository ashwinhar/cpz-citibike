"""Extract data from CitiBike webpage"""

import os
import re
import zipfile
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src_constants.extract_constants import (
    CITIBIKE_URL_PREFIX,
    CITIBIKE_URL,
    RAW_DATA_FOLDER,
    RE_PATTERN,
    RE_PATTERN_PREFIX_BOUND,
    YEAR_FLOOR,
)


def get_existing_citibike_files(folder_path: str = RAW_DATA_FOLDER) -> list:
    """
    Return list of existing raw data (as .zip files) in folder_path

    Returns:
        list of file names
    """

    existing_files = []
    for folder_path, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".zip"):
                existing_files.append(file)

    return existing_files


def find_all_downloadable_files(url: str = CITIBIKE_URL) -> list:
    """Go to URL for CitiBike data and find all available .zip files

    Args:
        url (str): URL to visit

    Returns:
        list: List of links where downloadable files live
    """
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    driver.implicitly_wait(5)

    zip_links = [
        elem.get_attribute("href")
        for elem in driver.find_elements(By.TAG_NAME, "a")
        if elem.get_attribute("href") and elem.get_attribute("href").endswith(".zip")
    ]

    driver.quit()

    print(f"Found {len(zip_links)} zip files.")

    return zip_links


def find_files_of_interest(
    zip_links: list,
    re_pattern: str = RE_PATTERN,
    prefix_bound: int = RE_PATTERN_PREFIX_BOUND,
    year_floor: int = 0,
) -> list:
    """Filter available zip files

    CitiBike has ill-defined naming for the zip files that it uploads. This function
    filters all the downloadable files in the website to just the ones we are interested in.

    Args:
        zip_links (list): List of all zip_links at CitiBike URL
        re_pattern (str): RegEx pattern to match files of interest
        prefix_bound (int): Substring index boundary for when link prefix ends.
        year_floor (int): First year of interest. Files indexed before this year are out-of-bounds.
    Returns:
        list: Filtered list of zip_links *without* link prefix
    """
    filtered_links = [
        link[prefix_bound:] for link in zip_links if re.match(re_pattern, link)
    ]
    year_bounded_links = [
        link for link in filtered_links if int(link[:4]) >= year_floor
    ]

    return year_bounded_links


def download_citibike_file(download_url: str, save_path: str) -> None:
    """Download single CitiBike data .zip file based on URL

    Args:
        download_url (str): URL of specific .zip file
        save_path (str): Where the .zip file will be saved locally
    """

    # Download the file
    response = requests.get(download_url, stream=True, timeout=300)
    with open(save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Downloaded {download_url} to {save_path}")


def download_files(
    data_folder: str,
    url: str,
    download_option: str = "missing",
    file_names: list = None,
) -> None:
    """Execute download process

    Args:
        data_folder (str): Full path of raw data folder, typically src_constants.RAW_DATA_FOLDER
        url (str): URL to download from, typically src_constants.extract_constants.CITIBIKE_URL
        download_option (str): Either "missing", which downloads "files of interest" that are
            missing from ../data/raw_citibike_data/ or "specific", which requires user to pass
            in a list of specific file names *without* the URL_PREFIX
        file_names (list): List of specific file names. Use if you set download_option='specific'
    """
    existing_files = get_existing_citibike_files(data_folder)
    downloadable_files = find_all_downloadable_files(url)
    files_of_interest = find_files_of_interest(
        downloadable_files,
        re_pattern=RE_PATTERN,
        prefix_bound=RE_PATTERN_PREFIX_BOUND,
        year_floor=YEAR_FLOOR,
    )

    if download_option == "missing":
        files_to_download = [
            file for file in files_of_interest if file not in existing_files
        ]
    else:
        files_to_download = file_names

    for file in files_to_download:
        file_download_path = CITIBIKE_URL_PREFIX + file
        if file_download_path in downloadable_files and file not in existing_files:
            save_path = os.path.join(RAW_DATA_FOLDER, file)
            print(f"Downloading {file_download_path} to {save_path}")
            download_citibike_file(file_download_path, save_path)
        else:
            if file not in downloadable_files:
                print(f"{file} not available for download")
            elif file in existing_files:
                print(f"{file} already in {RAW_DATA_FOLDER}")


def unzip_file_recursive(zip_file_path) -> None:
    """Recursively extract zip files within a given zip file"""

    # Unzip current file
    print(f"Attempting to unzip file at {zip_file_path}")
    extract_location = zip_file_path.replace(".zip", "")
    if zip_file_path.endswith(".zip"):
        if not os.path.isfile(extract_location) and not os.path.isdir(extract_location):
            try:
                with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                    print(f"Unzipping {zip_file_path} to {extract_location}")
                    zip_ref.extractall(extract_location)
            except zipfile.BadZipFile:
                print("Error: The file is not a valid zip archive.")
            except FileNotFoundError:
                print("Error: The zip file was not found.")
            except PermissionError:
                print("Error: Permission denied when accessing the file.")

        else:
            print("File or folder path already exists, unzipping operation passed")

    # Traverse into new folder
    if os.path.isdir(extract_location):
        for item in os.listdir(extract_location):
            item_path = os.path.join(extract_location, item)
            if (item.endswith(".zip") and os.path.isfile(item_path)) or (
                os.path.isdir(item_path) and not "MACOSX" in item_path
            ):
                unzip_file_recursive(item_path)
