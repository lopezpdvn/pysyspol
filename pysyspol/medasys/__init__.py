import json

def get_core_resources(core_resources_fp):
    with open(core_resources_fp) as coref:
        return json.load(coref)
