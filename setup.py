"""Basic setup"""

from setuptools import setup, find_packages

setup(
    name="cpz_citibike",
    version="0.1",
    packages=find_packages(where="src"),  # Ensure it finds the `src` directory
    package_dir={"": "src"},  # Set `src` as the base package directory
)
