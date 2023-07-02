from setuptools import find_packages, setup

setup(
    name="rssify",
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "beautifulsoup4",
        "requests",
        "rfeed",
    ],
)
