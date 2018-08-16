
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='fl33t',
    version='0.3.4',
    description='Fl33t API Client',
    long_description=readme(),
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
