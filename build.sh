#!/bin/bash
echo "*************** Installing requirements:"
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
echo "*************** Linting:"
flake8 .
echo "*************** Building package:"
python setup.py sdist bdist_wheel
echo "*************** Removing source files:"
rm -rf dir_compat
echo "*************** Installing package:"
pip install dist/dir_compat-0.2.2-py3-none-any.whl
echo "*************** Running tests:"
python -m unittest discover tests