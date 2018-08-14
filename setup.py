
from setuptools import setup

setup(
    name='fl33t',
    version='0.3.2',
    description='Fl33t API Client',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    url='https://github.com/fictivekin/fl33t-client',
    author='Fictive Kin LLC',
    author_email='hello@fictivekin.com',
    maintainer='Fictive Kin LLC',
    maintainer_email='systems@fictivekin.com',
    license='MIT',
    packages=['fl33t','fl33t.models'],
    install_requires=[
        'python-dateutil',
        'pytz',
        'requests',
    ],
)
