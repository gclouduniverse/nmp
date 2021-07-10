import sys

from setuptools import setup, find_packages


if sys.version_info < (3, 8):
    sys.exit("Sorry, Python < 3.8 is not yet supported")


setup(
    name="nmp",
    version="3",
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
    install_requires=["nbformat==5.1.*", "vaip=3.1"],
)
