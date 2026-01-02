from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in erpassist/__init__.py
from erpassist import __version__ as version

setup(
	name="erpassist",
	version=version,
	description="AI-powered assistant for ERPNext",
	author="Your Company",
	author_email="support@yourcompany.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
