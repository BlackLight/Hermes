import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

conf_file_path = os.path.join(os.getenv('HOME'), '.config', 'evesp')
print(conf_file_path)

setup(
    name = "evesp",
    # version = "TBD",
    install_requires = ['PyDispatcher>=2.0.5'],
    author = "Fabio Manganiello",
    author_email = "blacklight86@gmail.com",
    description = ("Evesp - EVEnt Socket Platform - a middleware infrastructure for events"),
    license = "Apache Licence 2.0",
    keywords = "evesp PingPoke middleware eventbus",
    url = "https://github.com/BlackLight/evesp",
    packages=['evesp'],
    long_description=read('README.md'),
    entry_points = {
        'console_scripts': [
            'evespd = evesp.__main__:_boot'
        ],
    },

    data_files = [
        (conf_file_path, ['evesp/evesp.conf.example'])
    ],

    classifiers = [
        "Development Status :: In Progress",
        "License :: OSI Approved :: Apache Licence 2.0",
    ],
)

