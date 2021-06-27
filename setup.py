from setuptools import setup, find_packages

setup(
    name="nmp",
    version="1",
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
