"""Module to load raw data into DuckDB database"""

import os
import duckdb
import pandas as pd
from src_constants.load_constants import DATABASE_PATH
from src_components.data_extraction.organize import find_month_folders


def get_database_connection(
    database_path: str = DATABASE_PATH,
) -> duckdb.DuckDBPyConnection:
    """
    Return connection to local DuckDB database

    Params:
        database_path - Absolute path
    Returns:
        DuckDBPyConnection
    """
    return duckdb.connect(database_path)


def create_table(
    db_conn: duckdb.DuckDBPyConnection, results_dataframe: pd.DataFrame, table_name: str
) -> None:
    """
    Create table in local DuckDB database

    Params:
        db_conn - Connection to local DuckDB database. Typically
            returned by get_database_connection()
        results_dataframe - Dataframe to create. Typically returned by extract_dataset()
        table_name - Full database object identifier

    """
    print(f"Creating {table_name}")
    statement = (
        f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM results_dataframe"
    )
    print(statement)
    db_conn.sql(statement)


def drop_table(db_conn: duckdb.DuckDBPyConnection, identifier: str) -> None:
    """
    Drop table if exists in local duckdb file

    Params:
        db_conn - Connection to local DuckDB database. Typically returned
            by get_database_connection()
        identifier - Database object to drop

    """
    statement = f"DROP TABLE IF EXISTS {identifier}"
    db_conn.sql(statement)


def create_schema(db_conn: duckdb.DuckDBPyConnection, schema_name: str) -> None:
    """
    Create schema in database if not exists

    Params:
        db_conn - Connection to local DuckDB database. Typically returned by
            get_database_connection()
        schema_name - Schema name as string
    """

    db_conn.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")


def create_all_tables() -> None:
    """
    Create all tables from .csv files in the data folder
    """
    create_schema(get_database_connection(), "staging")

    month_folders, missing_months, duplicate_months = find_month_folders()
    if len(missing_months) != 0 or len(duplicate_months) != 0:
        if missing_months is not None:
            print(f"Missing months exist: {missing_months}")
            print("You must resolve this before creating tables. Exiting process")
        if duplicate_months is not None:
            print(f"Duplicate months exist: {duplicate_months}")
            print("You must resolve this before creating tables. Exiting process")
    else:
        con = get_database_connection()
        month_folders.sort()
        for month in month_folders:
            for file in os.listdir(month):
                if file.endswith(".csv"):
                    renamed_file = file.replace("-", "_").replace(".csv", "")
                    print(f"Creating table {renamed_file}")
                    create_table(
                        con,
                        pd.read_csv(os.path.join(month, file)),
                        f'staging."{renamed_file}"',
                    )
