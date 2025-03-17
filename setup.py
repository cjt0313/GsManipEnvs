from setuptools import setup, find_packages

setup(
    name="gsmanipenvs",
    version="0.1",
    packages=find_packages(where="src"),  # Look inside `src/`
    package_dir={"": "src"},  # Root of the package code is `src/`
    install_requires=[],  # Add dependencies here
)