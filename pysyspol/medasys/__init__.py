import json
import logging

def get_core_resources(core_resources_fp):
    with open(core_resources_fp) as coref:
        return json.load(coref)

def logging_config(msgfmt='[{0}]: %(message)s', prgname=None,
        level=logging.INFO):
    logging.basicConfig(format=msgfmt.format(prgname), level=level)
