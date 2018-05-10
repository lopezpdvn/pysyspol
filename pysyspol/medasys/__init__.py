import sys
import json
import logging
from os import access, R_OK, walk
from os.path import join, sep
from itertools import chain

from pysyspol.util import get_script_name

def get_core_resources(core_resources_fp):
    with open(core_resources_fp) as coref:
        return json.load(coref)

def logging_config(prgname=None, msgfmt='[{0}]: %(message)s',
        level=logging.INFO):
    '''Deprecated'''
    print('Function `pysyspol.medasys.logging_config` is deprecated',
            file=sys.stderr)
    prgname = get_script_name() if not prgname else prgname
    logging.basicConfig(format=msgfmt.format(prgname), level=level)

def get_tagged_resources(resources, tags=()):
    return (resource for tag in tags for resource in resources
            if tag in resource['tags'])

def validate_paths(resources, resources_fp):
    valid = True
    for resource in resources:
        for path in resource['path']:
            path = join(resources_fp, path)
            if not access(path, R_OK):
                logging.error('Resource `{}` not readable'.format(path))
                valid = False
    if valid:
        logging.info('All resources exist and readable')
    else:
        logging.error('Some errors happened trying to read resources')

    return valid

def get_valid_tags(tags_fp):
    with open(tags_fp) as tagsf:
        tag_entries = json.load(tagsf)
    return chain.from_iterable(tag['id'] for tag in tag_entries)

def validate_tags(resources, tags_fp):
    valid_tags = tuple(get_valid_tags(tags_fp))
    valid = True
    for resource in resources:
        for tag in resource['tags']:
            if tag not in valid_tags:
                logging.error('Tag `{}` of resource `{}` not valid'.format(
                    tag, resource['path']))
                valid = False
    if valid:
        logging.info('All tags are valid')
    else:
        logging.error('Some errors happened trying to validate tags')
    return valid

def get_tags(resources):
    return sorted(set(chain.from_iterable(i['tags'] for i in resources)))

def get_all_resources(resources_fp, approot_fp):
    for relpath, dirs, files in walk(resources_fp):
        if relpath == approot_fp:
            dirs[:] = []
            continue
        for f in files:
            yield join(relpath, f).replace(resources_fp, '').strip(sep)

def get_matched_resource(resource_path, core_resources, resources_path):
    matches = []
    resource_path = resource_path.lower()

    i = 0
    for resource in core_resources:
        for path in resource['path']:
            if resource_path in path.lower():
                matches.append((i, resource))
        i += 1

    if len(matches) > 1:
        raise ValueError(
                'len(matches) > 1, can only edit one resource at a time')

    if len(matches) == 1:
        return matches[0]

    matches = []
    for relpath, dirs, files in walk(resources_path):
        if matches:
            break
        for fname in files:
            if resource_path in fname.lower():
                matches.append((-1, join(relpath, fname)))
                break

    if not matches:
        raise ValueError('No matched core resource')

    return matches[0]
