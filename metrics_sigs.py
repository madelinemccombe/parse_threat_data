####!/usr/bin/env python3
"""
Parse data files with json output for estack bulk load
"""

from datetime import datetime
import json
import conf
import csv
import sys


def metrics_sigs():
    """
    daily signature counts
    """

    input_file = f'{conf.input_dir}/{conf.sig_input_file}'

    # timestamp to be added to the file name
    filedate = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')

    # generate list of all filetypes and check for missing elements before processing data
    with open(input_file, 'r') as sig_file:
        sigs_csv = csv.reader(sig_file, delimiter=',')
        next(sigs_csv)
        filetype_list = []
        for row_list in sigs_csv:
            file_type = row_list[2]

            if file_type in filetype_list:
                pass
            else:
                filetype_list.append(file_type)

    # check that all filetypes are captured
    # if any are missing stop and user has to update the file list in conf.py
    missing_filetypes = []
    for filetype in filetype_list:
        if filetype in conf.sigfiletypes:
            pass
        else:
            missing_filetypes.append(filetype)

    if len(missing_filetypes) > 0:
        print('found missing filetypes')
        print(missing_filetypes)
        sys.exit()

    # create empty json output file
    with open(f'{conf.output_dir}/{conf.sig_output_file}-{filedate}.json', 'w') as f:
        print(f'writing to file: {conf.output_dir}/{conf.sig_output_file}-{filedate}.json')

    # iterate across the csv rows and output json elk entries
    with open(input_file, 'r') as sig_file:
        sigs_csv = csv.reader(sig_file, delimiter=',')
        next(sigs_csv)
        for row_list in sigs_csv:
            row_date = row_list[1]
            date_datetime = datetime.strptime(row_date, '%Y/%m/%d')

            stats_dict = {}
            stats_dict['date'] = date_datetime.strftime('%Y-%m-%dT00:00:00Z')
            stats_dict['metrics.threat.signatures.filetype.raw'] = row_list[2]
            stats_dict['metrics.threat.signatures.count'] = int(row_list[3])

            # add other naming conventions for file type names
            filetype = row_list[2]
            stats_dict['metrics.threat.signatures.filetype.group'] = conf.sigfiletypes[filetype][0]
            stats_dict['metrics.threat.signatures.filetype.autofocus'] = conf.sigfiletypes[filetype][1]

            # create elk index by month and year
            index_tag_full = {}
            index_tag_inner = {}
            elk_index_name = f"threat-signatures-{date_datetime.year}-{date_datetime.strftime('%m')}"
            index_tag_inner['_index'] = f'{elk_index_name}'
            index_tag_inner['_type'] = '_doc'
            index_tag_full['index'] = index_tag_inner

            # write elk formated json file
            with open(f'{conf.output_dir}/{conf.sig_output_file}-{filedate}.json', 'a') as file:
                file.write(json.dumps(index_tag_full, indent=None, sort_keys=False) + "\n")
                file.write(json.dumps(stats_dict, indent=None, sort_keys=False) + "\n")


    # print out the elasticSearch bulk load curl commands
    print('\nUse curl -XDELETE [url]:[port]/index to delete data from the index')
    print('use the XPOST curl command to load json data to elasticSearch')
    print('add -u with username:password if security features enabled\n')

    print(
        f'curl -s -XPOST \'http://{conf.elastic_url_port}/_bulk\' --data-binary @{conf.output_dir}/{conf.sig_output_file}-{filedate}.json -H \"Content-Type: application/x-ndjson\" \n')


if __name__ == '__main__':
    metrics_sigs()
