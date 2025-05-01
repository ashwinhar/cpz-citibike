# CitiBike Analysis - Transportation Alternatives
You can use this repo to set up your own local DuckDB database analyzing CitiBike data. Out of the box, it will automatically detect files uploaded to the CitiBike website that you don't have locally, download them, and organize the files. 

It will also use the raw data to create fact tables within the DuckDB database for you to query, all of which is documented in the [dbt docs site](https://ashwinhar.github.io/cpz-citibike/#!/overview) for this project. 

**Note that onboarding new months of data not already included in the repo will require manual intervention which is documented below**. Automatically adding new data sources is error prone, since CitiBike uploads data in inconsistent file formats. Instead of creating an automatic process, I chose to carefully define a manual process to do the onboarding. Peeking inside `src/src_components/data_transform/models/staging/_staging_2025__sources.yml` will show you the most recent month of data. 

## Setup
1. Install the appropriate [conda](anaconda.org) version for your machine, and install [VSCode](https://code.visualstudio.com/)
2. Open your terminal, and navigate to the root directory (`cpz_citibike`)
3. Run `conda env create -f /configs/environment.yml -n cpz-citibike`
4. Run `conda activate cpz-citibike` if the conda enviornment hasn't been activated yet
5. Run `pip install -e .` inside the conda environment
6. Navigate to `src/src_components/data_transform/` and make sure there is a `dev.duckdb` file. If there isn't, make a new empty file with that name. 
7. Modify `PARENT_DIR` in `src/src_constants/extract_constants.py` to match the root directory of your repo. 

Follow the ELT steps below to use `nbs/eda.ipynb` to access the database, either via SQL or Python. 

## Extracting data (**E**LT)
Navigate to `nbs/data_extraction.ipynb` within VSCode. Data extraction uses a "driver" function called `download_files` which will download all relevant files that don't currently exist within your `data/raw_citibike_data/` directory. 

Any constants that are listed below will be defined in `src/src_constants/extract_constants.py`. Run the notebook cells *one-by-one*. All the stages are explained below, but the notebook run is very easy. You should only need to manually intervene **once**. 

### Stage 1: Determine existing files
`download_files` will first call a function called `get_existing_citibike_files`. This function will "walk" through a given folder path (by default, this is `RAW_DATA_FOLDER`) and return all zip file names as a list. CitiBike always uploads zip files, not unzipped csv files. 

### Stage 2: Find all downloadable files
`download_files` will then run `find_all_downloadable_files`, which simply navigates to a URL (`CITIBIKE_URL`) and returns all the zip files that are available to download as a list. 

### Stage 3: Filter downloadable files to *only* files of "interest"
`download_files` will then run `find_files_of_interest`. There are a bunch of zip files we wouldn't be interested in, and we want to filter them out. We will filter out files that don't fit the RegEx pattern defined by `RE_PATTERN`, and chop off the link prefix. For example, for a downloadable file we might get:
```
https://s3.amazonaws.com/tripdata/202501-citibike-tripdata.zip"
```

It's confusing to keep seeing that link prefix repeated when you're analyzing a data extract run, so the function will lop off the prefix and return only 
```
[202501-citibike-tripdata.zip]
```

By default, `download_files` will figure out which valid files are "missing" from your data directory and then download those. In the case that you want to download a specific file from the CitiBike website, you can pass in `download_option="specific"` and then pass in a list of `file_names`. Make sure that the file names are given without the link prefix. 

### Stage 4: Recursively unzipping files
Follow the instructions in the notebook by either passing `RAW_DATA_FOLDER` or the absolute path of the zip file you want to unzip to `unzip_file_recursive()`. CitiBike sometimes creates a "zip folder of zip folders", which is why this is a recursive unzip. 

### Stage 5: Cleanup and organize
We use a driver function called `cleanup_and_organize` to organize the zip files and .csv files. There are three functions that are called here. 

1. `remove_redundant_subfolders` - Sometimes CitiBike nests month folders with the same name. For example, if there is a folder called `2020-citibike-tripdata` and all .csv files are stored in a subfolder called `2020-citibike-tripdata`, move all .csv files up into the parent folder with the same name, and remove the redundant subfolder.
2. `relocate_zip_files` - Moves zip files into their own folder called `zip_files`
3. `reorganize_month_files` - Standardizes where the .csv files live into a specific folder structure. Specifically:
```
data/raw_citibike_data/
├── YYYY-citibike-tripdata/
│   ├── YYYYMM-citibike-tripdata/
│   │   ├── YYYYMM-citibike-tripdata_1.csv
│   │   ├── YYYYMM-citibike-tripdata_2.csv
│   │   └── ...
```

## Loading data (E**L**T)
Navigate to `nbs/data_load.ipynb`

### Stage 1: Create staging tables that don't already exist
`create_all_tables` will automatically skip creating tables that already exist. Simply run the cell. 

### Stage 2: Load geojson
Transportation Alternatives has provided a geojson that defines the Congestion Pricing zone. That file is available in `configs/`. Run `create_polygon` to load this polygon into the database.


## Transforming data (EL**T**)
Every time you onboard a new month of data, you will need to manually make some adjustments to the files within `src/src_components/data_transform/models/staging`. Automatically making these changes is too error-prone and unnecessary for this project.

### How to onboard a new month of data

First, navigate to the appropriate staging file in `src/src_components/data_transform/models/staging` that corresponds to the year the new month of data lives in. For example, when I want to onboard data for March 2025 I would navigate to `_staging_2025__sources.yml`. 

Copy the most recent section of the file that starts with `- name: YYYYMM_citibike_tripdata` (it should be around 35 lines) and paste it directly below at *the same level*. For example, the bottom of my file might look like:

```
- name: 202502_citibike_tripdata_3
  description: "{{ doc('tbl_staging_XXXXXX_citibike_tripdata_X')}}"
  columns:
    - name: ride_id
    description: "{{ doc('col_ride_id')}}"
    data_tests:
        - unique
    - name: rideable_type
    description: "{{ doc('col_rideable_type')}}"
    data_tests:
        - accepted_values:
            values: ['electric_bike', 'classic_bike']
    ...
```

Now it should look like: 

```
- name: 202502_citibike_tripdata_3
  description: "{{ doc('tbl_staging_XXXXXX_citibike_tripdata_X')}}"
  columns:
    - name: ride_id
    description: "{{ doc('col_ride_id')}}"
    data_tests:
        - unique
    - name: rideable_type
    description: "{{ doc('col_rideable_type')}}"
    data_tests:
        - accepted_values:
            values: ['electric_bike', 'classic_bike']
    ...
- name: 202502_citibike_tripdata_3 <-- MODIFY THIS NAME
  description: "{{ doc('tbl_staging_XXXXXX_citibike_tripdata_X')}}"
  columns:
    - name: ride_id
    description: "{{ doc('col_ride_id')}}"
    data_tests:
        - unique
    - name: rideable_type
    description: "{{ doc('col_rideable_type')}}"
    data_tests:
        - accepted_values:
            values: ['electric_bike', 'classic_bike']
    ...
```

You'll have to paste this code block for **as many new csv files you have downloaded and loaded to duckdb in the data_load.ipynb notebook**. Go to `data/raw_citibike_data/` if you're not sure. Modify the name to match the name of each one of the new .csv files without the file extension. For example, if I downloaded a new file called `202503-citibike-tripdata.csv` I should change the line indicated above to: 

```
- name: 202503_citibike_tripdata
```

Next, navigate to `src/src_components/data_transform/models/intermediate`, specifically the appropriate year folder. In this example, it would be `yr_2025`. Duplicate any one of the files fitting the `mmm_YYYY.sql` format and rename it appropriately. For example, I can duplicate `feb_2025.sql` and rename to `mar_2025.sql`

Modify this new file at the very top to match all the new sources you added to the staging file, making sure to `UNION ALL` every time. For example, let's say March 2025 actually had two files I added to the .yml file above called `202503_citibike_tripdata_1` and `202503_citibike_tripdata_2`: 

```
with cte as (
    select * from {{ source('staging_2025', '202503_citibike_tripdata_1') }} 
    UNION ALL 
    select * from {{ source('staging_2025', '202503_citibike_tripdata_2') }} 
)
```

Now, go to the appropriate "year" file that's in that same directory. In this example, it's `yr_2025`. Then, match the format at the top of the file to `UNION ALL` the new month file. For example, the top of the file would change from: 

```
with cte as (
    select * from {{ref ("jan_2025")}}
    UNION ALL
    select * from {{ref ("feb_2025")}}
)
```
to 
```
with cte as (
    select * from {{ref ("jan_2025")}}
    UNION ALL
    select * from {{ref ("feb_2025")}}
    UNION ALL 
    select * from {{ref ("mar_2025")}}
)
```

Finally, go to the `__schema.yml` file you see in the same directory. In this example, it would be `_yr_2025__schema.yml`. Copy-paste one of the month sections, and modify the name to match teh new month you onboarded. 

### What to do if you are in a new year, and don't see the appropriate files