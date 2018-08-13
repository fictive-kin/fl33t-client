
from setuptools import setup

setup(
    name='fl33t',
    version='0.2.2',
    description='Fl33t API Client',
    url='https://github.com/fictivekin/fl33t-client',
    author='Fictive Kin LLC',
    author_email='hello@fictivekin.com',
    maintainer='Fictive Kin LLC',
    maintainer_email='systems@fictivekin.com',
    packages=['fl33t'],
    install_requires=[
        'python-dateutil',
        'pytz',
        'requests',
    ],
)
