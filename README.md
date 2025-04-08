# CitiBike Analysis - Transportation Alternatives
You can use this repo to set up your own local DuckDB database analyzing CitiBike data. Out of the box, it will automatically detect files uploaded to the CitiBike website that you don't have locally, download them, and organize the files. 

It will also use the raw data to create fact tables within the DuckDB database for you to query, all of which is documented in the [dbt docs site](https://ashwinhar.github.io/cpz-citibike/#!/overview) for this project. 

**Note that onboarding new months of data not already included in the repo will require manual intervention which is documented below**. Automatically adding new data sources is error prone, since CitiBike uploads data in inconsistent file formats. Instead of creating an automatic process, I chose to carefully define a manual process to do the onboarding. Peeking inside `src/src_components/data_transform/models/staging/_staging_2025__sources.yml` will show you the most recent month of data. 

## Setup
1. Install the appropriate [conda](anaconda.org) version for your machine
2. Open your terminal, and navigate to the root directory (`cpz_citibike`)
3. Run `conda env create -f /configs/environment.yml -n cpz-citibike`
4. Run `conda activate cpz-citibike` if the conda enviornment hasn't been activated yet
5. Run `pip install -e .` inside the conda environment
6. Navigate to `src/src_components/data_transform/` and make sure there is a `dev.duckdb` file. If there isn't, make a new empty file with that name. 
7. Run `dbt run`
8. If you want to re-generate documentation, you should run `dbt docs generate` and then `dbt docs serve`. Remember that any commands that start with `dbt` should be run within `src/src_components/data_transform/`. 

You can now use `nbs/eda.ipynb` to access the database, either via SQL or Python. 

## Extracting Data
