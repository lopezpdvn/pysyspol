import sys
import os
from random import SystemRandom
from string import ascii_letters, digits
from os.path import abspath, dirname, basename, splitext
from inspect import getfile

ALPHA_NUMERIC_STR = ascii_letters + digits

sys_random = SystemRandom()

def random_alphanumeric_str(n):
    return ''.join(sys_random.choice(ALPHA_NUMERIC_STR) for i in range(n))

def getdir(obj):
    '''Return dir of file in which object is defined

    Example:

      import inspect
      script_dir = getdir(inspect.currentframe())
    '''
    return dirname(abspath(getfile(obj))).rstrip(os.sep)

def get_script_name():
    return splitext(basename(sys.argv[0]))[0]
