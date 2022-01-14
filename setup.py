from setuptools import setup

setup(
    name='pyPSON',
    author='lechos22',
    license='BSD 3-Clause License',
    description='module for parsing and dumping PSON',
    version='1.0.0',
    package_dir={'pson': 'pson'},
    packages=['pson'],
    # scripts=['pson/pson_prettify.py', 'pson/pson_to_json.py', 'pson/json_to_pson.py']
)
