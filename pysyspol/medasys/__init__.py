import json
import logging
from pysyspol.util import get_script_name

def get_core_resources(core_resources_fp):
    with open(core_resources_fp) as coref:
        return json.load(coref)

def logging_config(prgname=None, msgfmt='[{0}]: %(message)s',
        level=logging.INFO):
    prgname = get_script_name() if not prgname else prgname
    logging.basicConfig(format=msgfmt.format(prgname), level=level)

def get_tagged_resources(resources, tags=()):
    return (resource for tag in tags for resource in resources
            if tag in resource['tags'])
