from setuptools import setup, find_packages

setup(
    name='dir_compat',
    description='Directory compatibility checker',
    version='0.2.2',
    url='https://pypi.org/project/dir_compat',
    author='Illia Deinega',
    packages=find_packages(),
    entry_points={'console_scripts': [
        'dir_compat = dir_compat.main:run'
    ]}
)
