"""Organize extracted files"""

from datetime import datetime
import os
import shutil
import re
from src_constants.extract_constants import RAW_DATA_FOLDER


def remove_redundant_subfolders(root_dir: str = RAW_DATA_FOLDER) -> None:
    """Remove redundant subfolders from parent folder with same name, if exists.

    For example, if there is a folder called "2020-citibike-tripdata" and all .csv
    files are stored in a subfolder called "2020-citibike-tripdata", move all .csv
    files up into the parent folder with the same name, and remove the redundant subfolder.

    Args:
        root_dir (str) - Directory containing all data files to process
    """
    for folder in os.listdir(root_dir):
        parent_folder_path = os.path.join(root_dir, folder)

        if os.path.isdir(parent_folder_path):
            subfolder_path = os.path.join(parent_folder_path, folder)

            if os.path.exists(subfolder_path) and os.path.isdir(subfolder_path):
                print(f"Duplicate subfolder found at {subfolder_path}")
                for item in os.listdir(subfolder_path):
                    print(f"Moving {item} to {parent_folder_path}")
                    shutil.move(os.path.join(subfolder_path, item), parent_folder_path)
                print(f"Removing duplicate subfolder at {subfolder_path}")
                os.rmdir(subfolder_path)  # Remove empty duplicate folder


def relocate_zip_files(root_dir: str = RAW_DATA_FOLDER) -> None:
    """Move zip files into their own directory called "zip_files"

    Args:
        root_dir (str) - Directory containing all data files to process
    """
    # Create folder "zip_files" if it doesn't already exist
    zip_folder = os.path.join(root_dir, "zip_files")
    if not os.path.exists(zip_folder):
        print(f"Folder {zip_folder} does not currently exist. Creating {zip_folder}")
        os.mkdir(zip_folder)

    # Walk through all subdirectories, and move .zip files into /zip_files/
    for folder_path, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".zip") and "zip_files" not in folder_path:
                file_path = os.path.join(folder_path, file)
                print(f"Moving {file_path} to {zip_folder}")
                shutil.move(file_path, zip_folder)


def reorganize_month_files(root_dir: str = RAW_DATA_FOLDER) -> None:
    """Move month-specific folders to a different folder, corresponding to the year.

    CitiBike sometimes uploads data in a directory called YYYYMM-citibike-data, instead
    of a folder called YYYY-citibike-data, and then having all YYYYMM-citibike-data folders
    inside it. This causes validation issues. This standardizes how the files are organized.

    Args:
        root_dir (str) - Directory containing all data files to process
    """

    month_folder_pattern = re.compile(
        r"\b(\d{4})\d{2}-citibike-tripdata\b"
    )  # Matches YYYYMM-tripdata
    month_folders = []

    # Find "month-specific" folders in root directory that match pattern YYYYMM-citibike-tripdata
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder)
        if os.path.isdir(folder_path):
            match = month_folder_pattern.match(folder)
            if match:
                print(f"Found month-specific folder at {folder}")
                year = match.group(1)
                month_folders.append((folder, year))

    # Move month-specific folders into their own directory called YYYY-citibike-tripdata
    for folder, year in month_folders:
        year_folder = os.path.join(root_dir, f"{year}-citibike-tripdata")
        if not os.path.exists(year_folder):
            print(
                f"Year-specific folder {year_folder} does not exist. Creating {year_folder}"
            )
            os.mkdir(year_folder)
        print(f"Moving {folder} to {year_folder}")
        shutil.move(os.path.join(root_dir, folder), year_folder)


def cleanup_and_organize(root_dir: str = RAW_DATA_FOLDER):
    """Execute series of organization steps for extracted files

    Args:
        root_dir (str) - Directory containing all data files to process
    """
    remove_redundant_subfolders(root_dir)
    relocate_zip_files(root_dir)
    reorganize_month_files(root_dir)


def find_month_folders(root_dir: str = RAW_DATA_FOLDER):
    """Find all month folders in the root directory

    List all month folders, find missing months in previous years, and detect duplicate months

    Args:
        root_dir (str) - Directory containing all data files to process
    Returns:
        month_folders (list) - List of month folders found
        missing_months (dict) - Dictionary of missing months in previous years
        duplicate_months (dict) - Dictionary of duplicate months
    """
    month_folders = []
    missing_months = {}
    duplicate_months = {}
    current_year = datetime.now().year

    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            # Check if the folder name starts with YYYYMM
            match = re.match(r"^(\d{6})", directory)
            if match:
                month_folders.append(os.path.join(root, directory))

    # Organizing found months by year
    year_months = {}
    month_occurrences = {}
    for path in month_folders:
        folder_name = os.path.basename(path)
        year, month = int(folder_name[:4]), int(folder_name[4:6])
        year_months.setdefault(year, set()).add(month)
        month_occurrences.setdefault((year, month), []).append(path)

    # Checking for missing months in previous years
    for year, months in year_months.items():
        if year < current_year:
            missing = set(range(1, 13)) - months
            if missing:
                missing_months[year] = sorted(missing)

    # Checking for duplicate month folders
    for (year, month), paths in month_occurrences.items():
        if len(paths) > 1:
            duplicate_months[(year, month)] = paths

    return month_folders, missing_months, duplicate_months
