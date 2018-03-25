import sys
import os
import logging
from random import SystemRandom
from string import ascii_letters, digits
from os.path import abspath, dirname, basename, splitext
from inspect import getfile

ALPHA_NUMERIC_STR = ascii_letters + digits
LOG_MSG_FMT_DEFAULT = '[{0}]: %(message)s'

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

def logging_config(prgname=None, msgfmt=LOG_MSG_FMT_DEFAULT,
        level=logging.INFO):
    '''Most basic logging configuration with default values'''
    prgname = get_script_name() if not prgname else prgname
    logging.basicConfig(format=msgfmt.format(prgname), level=level)
