#!/usr/bin/env python3
import sys
import os
import os.path
import json
import time
import csv

from panafapi_hacked import panafapi_hacked
from datetime import date, timedelta, datetime
from collections import OrderedDict


def main():

    libpath = os.path.dirname(os.path.abspath(__file__))
    sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
    thismodule = sys.modules[__name__]

# Vistoq api_key
#    api_key = '173a6172-6256-4ec6-a085-67ac3f57f6d1'
# Palo Alto api_key
    api_key = 'c274ae6d-9754-4c3c-abe3-3acf60a9b953'
# Demo devices api_key
#    api_key = '7fac67a8-6022-4693-9298-e36cab3d8192'
    hostname = 'autofocus.paloaltonetworks.com'

    start_new_output_file = True

# Scopes used are global and public
    scope = 'global'

# Verdict options as all or malware to set the query
    verdict = 'all'

# Query type for sample search mapped to the dictionary with same name
    query_type = 'region'

    query_count = OrderedDict([])
    weeks = 52
#   base init_date for past 1 year: init_date = date.today()-timedelta(days=372)
    init_date = date.today()-timedelta(days=372)

# Sample tag group query that is base for iteration across time (monthly) and tag Group value
# {"query":{"operator":"all","children":[{"field":"sample.malware","operator":"is","value":1},{"field":"sample.tag_group","operator":"is","value":"Ransomware"},{"field":"sample.create_date","operator":"is in the range","value":["2017-11-03T00:00:00","2017-11-03T23:59:59"]}]},"scope":"global","size":1,"from":0,"sort":{"create_date":{"order":"desc"}}}

    tag_group = [
                    'AdWare',
                    'Android',
                    'BankingTrojan',
                    'ExploitKit',
                    'FileInfector',
                    'HackingTool',
                    'Linux',
                    'OSX',
                    'PointofSale',
                    'Ransomware',
                    'Worm',
                    ]


    upload_source = [
                'Firewall',
                'Proofpoint',
                'Traps',
                'Traps Android',
                'Manual API',
                'WF Appliance',
                ]


    region = [
                'us',
                'eu',
                'jp',
                'sg',
                ]

    filetype = [
                "7zip Archive",
                "Adobe Flash File",
                "Android APK",
                "Apple's Universal binary file",
                "DLL",
                "DLL64",
                "ELF",
                "JAVA Class",
                "Email Link",
                "JAVA JAR",
                "Link",
                "Mac OS X app bundle in ZIP archive",
                "Mac OS X app installer",
                "MacOSX DMG",
                "Mach-O",
                "Microsoft Excel 97 - 2003 Document",
                "Microsoft Excel Document",
                "Microsoft PowerPoint 97 - 2003 Document",
                "Microsoft PowerPoint Document",
                "Microsoft Word 97 - 2003 Document",
                "Microsoft Word Document",
                "PDF",
                "PE",
                "PE64",
                "RAR Archive",
                "RTF"
                ]

# set conditionals based on the query_type
# field is the filter field of interest
# the field value is part of the iteration per the query_type dictionary
# output csv filename is query_type specific + scope and verdict appends
    if query_type == 'group':
        query_field = 'sample.tag_group'
        query_list = tag_group
        filename = 'tag_group_data_{0}_{1}.csv'.format(verdict,scope)

    if query_type == 'upload_source':
        query_field = 'session.upload_src'
        query_list = upload_source
        filename =  'upload_source_data_{0}_{1}.csv'.format(verdict,scope)

    if query_type == 'region':
        query_field = 'session.region'
        query_list = region
        filename = 'region_data_{0}_{1}.csv'.format(verdict,scope)


    print('\nStarting Autofocus queries for query_type = {0}'.format(query_type))
    print('Searching samples with verdict = {0}'.format(verdict))
    print('Searching samples with scope = {0}\n'.format(scope))

    FMT = "%H:%M:%S"
    start_time = datetime.now().strftime(FMT)
    print('Start time = {0}'.format(start_time))

  
    if start_new_output_file == True:

# Add in headers for the dict data
# Week label and then iterate across list items
        query_count['headers'] = ['Week']
        for item in query_list:
            query_count['headers'].append(item)

        with open(filename, 'w') as outfile:
            writer = csv.writer(outfile, delimiter=",", lineterminator="\n")
            for row_cells in query_count.values():
                writer.writerow(row_cells)


    start_date, end_date = init_date, init_date+timedelta(days=6)

# Iterate over weeks - count specified as weeks above

    for i in range(weeks):
        query_count = OrderedDict([])
        print("\nQuery time range between {0} and {1}".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
        query_count[start_date.strftime("%Y-%m-%d")] = [start_date.strftime("%Y-%m-%d")]

# For each week iterate over each list and get counts per item
# When list of items complete then append to csv file

        for item in query_list:

            print('\nworking with item = {0}\n'.format(item))

# query verdict conditional: malware or all
            if verdict == 'malware':
                query_arg = '{{"query":{{"operator":"all","children":[{{"field":"sample.malware","operator":"is","value":1}},{{"field":"{0}","operator":"is","value":"{1}"}},{{"field":"sample.create_date","operator":"is in the range","value":["{2}T00:00:00","{3}T23:59:59"]}}]}},"scope":"{4}","size":1,"from":0,"sort":{{"create_date":{{"order":"desc"}}}}}}'.format(query_field, item, start_date, end_date, scope)
            elif verdict == 'all':
                query_arg = '{{"query":{{"operator":"all","children":[{{"field":"{0}","operator":"is","value":"{1}"}},{{"field":"sample.create_date","operator":"is in the range","value":["{2}T00:00:00","{3}T23:59:59"]}}]}},"scope":"{4}","size":1,"from":0,"sort":{{"create_date":{{"order":"desc"}}}}}}'.format(query_field, item, start_date, end_date, scope)

            af_output = panafapi_hacked(hostname, api_key, 'sample_stats', query_arg)
            af_output_dict = json.loads(af_output)
            print('\nTotal for {0}: {1}\n'.format(item, af_output_dict['total']))
            query_count[start_date.strftime("%Y-%m-%d")].append(af_output_dict['total'])
            time.sleep(5) # time delay to ensure no per-minute quota exhaust
        
        start_date, end_date = end_date+timedelta(days=1), end_date+timedelta(days=7)

        with open(filename, 'a') as outfile:
            writer = csv.writer(outfile, delimiter=",", lineterminator="\n")
            for row_cells in query_count.values():
                writer.writerow(row_cells)

        updated_time = datetime.now().strftime(FMT)
        print('Current time = {0}'.format(updated_time))
        current_runtime = datetime.strptime(updated_time, FMT) - datetime.strptime(start_time, FMT)
        print('Current runtime = {0}'.format(current_runtime))

    print('\nQueries completed')
    updated_time = datetime.now().strftime(FMT)
    print('Current time = {0}'.format(updated_time))
    current_runtime = datetime.strptime(updated_time, FMT) - datetime.strptime(start_time, FMT)
    print('Final runtime = {0}'.format(current_runtime))


if __name__ == '__main__':
    main()






            
