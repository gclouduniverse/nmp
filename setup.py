import sys

from setuptools import setup, find_packages


if sys.version_info < (3, 8):
    sys.exit("Sorry, Python < 3.8 is not yet supported")


setup(
    name="nmp",
    version="2",
    author="Viacheslav Kovalevskyi",
    author_email="viacheslav@kovalevskyi.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "nmp = nmp.cli:main"
        ]
    },
    url="http://pypi.python.org/pypi/nmp/",
    license="LICENSE",
    description="Notebook Model Packager for Vertex AI",
    install_requires=open("requirements.txt").read().split("\n"),
)
