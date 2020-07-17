from setuptools import setup, find_packages
import pkg_resources
import pathlib

import src

with pathlib.Path("requirements.txt").open() as requirements_txt:
    requires = [ str(r) for r in pkg_resources.parse_requirements(requirements_txt) ]

setup(
    name = 'analyze_role',
    version = src.__version__,
    packages = find_packages(),
    entry_points = {
        'console_scripts': [ 'analyze_role=src.run_parliament:main']
    },
    install_requires = requires
)
