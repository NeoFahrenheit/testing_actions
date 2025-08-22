#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file is responsible for extracting the bump type from a commit message.
"""

import argparse

def extract(commit_message: str) -> str:
    """Extracts the bump type from the last commit message.
    The bump type must be in the format:

        fix(test): random message Bump:type

    The `Bump:type` must be at the end of the commit message.

    Only types accepted are: `['major', 'minor', 'patch']`.
    Everything else returns `error`.

    If no `Bump:` string is found in the commit message, 
    it defaults to `patch`.

    Args:
        commit_message (str): The last commit message.

    Returns:
        str: The build type. If parsing fails, returns `error`. 
        Else, returns the bump type.
    """    

    index = commit_message.find('Bump:')
    if index < 0:
        return 'patch'
    
    bump_type = commit_message[index:].split(':')[1].strip()
    if ' ' in bump_type:
        return 'error'
    
    if bump_type == 'build':
        # Build type must be done mannualy.
        return 'error'
    
    if bump_type in ['major', 'minor', 'patch']:
        return bump_type
    else:
        return 'error'
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract bump type from commit message.")
    parser.add_argument("commit", help="The last commit message")
    args = parser.parse_args()
    print(extract(args.commit))