from setuptools import setup


setup(
    name='nmp',
    version='1',
    author='Viacheslav Kovalevskyi',
    author_email='viacheslav@kovalevskyi.com',
    packages=['nmp'],
    scripts=[],
    url='http://pypi.python.org/pypi/nmp/',
    license='LICENSE',
    description='Notebook Model Packager for Vertex AI',
    install_requires=open('requirements.txt').read().split('\n'),
)
