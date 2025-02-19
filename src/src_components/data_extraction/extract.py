"""Extract data from CitiBike webpage"""

import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

CITIBIKE_URL = "https://s3.amazonaws.com/tripdata/index.html"
RAW_DATA_FOLDER = "data/raw_citibike_data"


def get_existing_citibike_data() -> list:
    """
    Return list of existing data in RAW_DATA_FOLDER

    Returns:
        list of file names
    """


def list_available_citibike_data() -> list:
    """
    Return full list of available data files in CITIBIKE_URL

    Returns:
        list of file names
    """


def download_absent_files() -> None:
    """
    Download files that don't already exist in RAW_DATA_FOLDER
    """


# Get the webpage content
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to fetch the webpage: {response.status_code}")
    exit()

# Parse the webpage
soup = BeautifulSoup(response.text, "html.parser")

# Find all links ending with .zip
zip_links = [
    a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith(".zip")
]

print(f"Found {len(zip_links)} zip files.")

# Download each zip file
for link in zip_links:
    zip_url = urljoin(url, link)
    zip_name = os.path.join(download_folder, os.path.basename(link))

    print(f"Downloading {zip_name}...")

    with requests.get(zip_url, stream=True) as r:
        r.raise_for_status()
        with open(zip_name, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"Downloaded {zip_name}")

print("All files downloaded successfully!")
