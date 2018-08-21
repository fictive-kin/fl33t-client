Contributing
============

Anyone is welcome to contribute fixes and enhancements to this project. We use:

- tox_ to run the test suite and linters
- for testing, we use pytest_
- for linting, we use both flake8_ and pylint_ with most settings enabled

Any pull request that modifies module code and has new functionality that does
not include tests will be blocked until tests have been written for it.

Testing
-------

Once you have written your new feature into the module, and have created a
test for it, please run the test. In order to run tests, you must
have tox_ installed::

     pip install tox

Then you can run it by simply typing::

     tox

Tox will create a virtual environment specifically for testing, so if you
have added requirements, ensure that they are listed in the `requirements.txt`
file and in the setup for distribution.

If it is a requirement only for testing, it should be listed in the
`requirements-test.txt` file.

.. note:: Please, ensure that your tests pass before submitting a PR.

Documentation
-------------

You do not need to create a virtual environment with all of the fl33t
dependencies to update documentation. Install the requirements listed in the
`requirements-docs.txt` file, and make your documentation changes. To
preview the documentation, run::

    make html

and then open the index file at `<repo>/docs/_build/index.html` in a browser
to verify that your changes are working before you submit a PR.

.. _tox: https://tox.readthedocs.io/en/latest/
.. _pytest: https://docs.pytest.org/en/latest/
.. _flake8: http://flake8.pycqa.org/en/latest/
.. _pylint: https://pylint.readthedocs.io/en/latest/
