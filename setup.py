from setuptools import setup, find_packages

setup(
	name="erpassist",
	version="0.0.1",
	description="AI-powered assistant for ERPNext",
	author="Your Company",
	author_email="support@yourcompany.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[
		"frappe",
		"openai>=1.0.0"
	]
)
