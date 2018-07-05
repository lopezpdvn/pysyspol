#!/usr/bin/env python
# coding=utf-8

'''flatten branches return by TFVC branch'''

# Standard library imports.
from __future__ import division
from pprint import pprint
import sys
import os
import atexit
import gc
import json

# Related third party imports.
# import third_party_mod

# Local application/library specific imports.
# import app_specific_mod

# Relevant ``__all__`` specification here.
# __all__ = ...

# GLOBAL CONSTANT names.  *if main* section at bottom sets global names too.

def on_exit():
    '''Actions to do on exit.'''

    # Invoke the garbage collector.
    gc.collect()

def main():
    '''Main program function.'''

    branches_dict = json.loads(sys.stdin.read())
    branches = [branch['path']
            for root_branch in branches_dict['value']
            for branch in traverse_branch_tree(root_branch, [])
            if branch['owner']['uniqueName'] == r'DOMAIN\username']
    json.dump(branches, sys.stdout)

def traverse_branch_tree(root_branch, stack):
    if not root_branch:
        return
    stack.append(root_branch)
    while stack:
        branch = stack.pop()
        yield branch
        for child in branch['children']:
            stack.append(child)

if __name__ == "__main__":
    # Program name from file name.
    PN = os.path.splitext(sys.argv[0])[0]

    # Log file.
    LOGF = ''.join([PN, '_log', '.txt'])

    atexit.register(on_exit)

    main()
