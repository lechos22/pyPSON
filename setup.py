from setuptools import setup

setup(
    name='pyPSON',
    author='lechos22',
    license='BSD 3-Clause License',
    description='module for parsing and dumping PSON',
    version='2.0.0',
    url="https://github.com/lechos22/pyPSON",
    package_dir={'': 'src'},
    packages=['pson'],
    # scripts=['pson/pson_prettify.py', 'pson/pson_to_json.py', 'pson/json_to_pson.py']
)
