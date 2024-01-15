from setuptools import setup, find_packages

setup(
    name='dir_compat',
    version='0.11',
    packages=find_packages(),
    entry_points={'console_scripts': [
        'dir-compat = dir_compat.main:run'
    ]}
)