"""a setup script for the package
source code are in the pypic directory
"""

from setuptools import setup, find_packages

setup(
    name="pypic",
    version="0.1",
    packages=find_packages(where="pypic"),
    package_dir={"": "pypic"},
)