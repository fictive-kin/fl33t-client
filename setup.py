
import os
import setuptools

def readme():
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'README.rst')) as f:
        return f.read()

name = 'fl33t'
description = 'Fl33t API Client'
version = '0.4.0'
author = 'Fictive Kin LLC'
email = 'hello@fictivekin.com'
classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development',
]

if __name__ == "__main__":
    setuptools.setup(
        name=name,
        version=version,
        description=description,
        long_description=readme(),
        classifiers=classifiers,
        url='https://github.com/fictivekin/fl33t-client',
        author=author,
        author_email=email,
        maintainer=author,
        maintainer_email=email,
        license='MIT',
        python_requires=">=3.4",
        packages=[
            'fl33t',
            'fl33t.models'
        ],
        install_requires=[
            'python-dateutil',
            'pytz',
            'requests',
        ],
    )
