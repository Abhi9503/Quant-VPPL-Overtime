from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in overtime_cal/__init__.py
from overtime_cal import __version__ as version

setup(
	name="overtime_cal",
	version=version,
	description="overtime calculation",
	author="erpdata",
	author_email="erpdata@erpdata.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
