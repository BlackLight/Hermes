import platform
import sys

if sys.version_info < (3,):
    sys.exit(
        'ERROR: evesp requires Python >= 3.0, but found %s.' %
        platform.python_version())

__version__ = 'git'

