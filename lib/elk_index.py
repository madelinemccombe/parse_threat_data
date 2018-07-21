####!/usr/bin/env python3
"""
Parse data files with json output for estack bulk load
"""

def elk_index(elk_index_name):

    """ Index setup for ELK Stack bulk install """

    index_tag_full = {}
    index_tag_inner = {}
    index_tag_inner['_index'] = elk_index_name
    index_tag_inner['_type'] = elk_index_name
    index_tag_full['index'] = index_tag_inner

    return index_tag_full

if __name__ == '__main__':
    elk_index()
