####!/usr/bin/env python3
"""
Parse data files with json output for estack bulk load
"""

from datetime import datetime
import json
from xlrd import open_workbook
import conf


def metrics_apps():
    """
    application daily counters for malware verdict samples

    """

    input_file = open_workbook(f'{conf.input_dir}/{conf.app_input_file}')
    input_sheet = input_file.sheet_by_name(conf.app_input_worksheet)

    # timestamp to be added to the file name
    filedate = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')

    # create empty json output file
    with open(f'{conf.output_dir}/{conf.app_output_file}-{filedate}.json', 'w') as f:
        print(f'writing to file: {conf.output_dir}/{conf.app_output_file}-{filedate}.json')

    # iterate across the worksheet rows and output json elk entries
    for row in range(2, input_sheet.nrows):
        row_date = input_sheet.cell(row, 0).value
        date_datetime = datetime.strptime(row_date, '%Y-%m-%d')

        stats_dict = {}
        stats_dict['date'] = date_datetime.strftime('%Y-%m-%dT00:00:00Z')
        stats_dict['metrics.threat.application.name'] = input_sheet.cell(row, 1).value
        stats_dict['metrics.threat.application.count'] = int(input_sheet.cell(row, 2).value)

        # create elk index by month and year
        index_tag_full = {}
        index_tag_inner = {}
        elk_index_name = f"metrics-threat-apps-{date_datetime.year}-{date_datetime.strftime('%m')}"
        index_tag_inner['_index'] = f'{elk_index_name}'
        index_tag_inner['_type'] = f'{elk_index_name}'
        index_tag_full['index'] = index_tag_inner

        # write elk formated json file
        with open(f'{conf.output_dir}/{conf.app_output_file}-{filedate}.json', 'a') as file:
            file.write(json.dumps(index_tag_full, indent=None, sort_keys=False) + "\n")
            file.write(json.dumps(stats_dict, indent=None, sort_keys=False) + "\n")


    # print out the elasticSearch bulk load curl commands
    print('\nUse curl -XDELETE [url]:[port]/index to delete data from the index')
    print('use the XPOST curl command to load json data to elasticSearch')
    print('add -u with username:password if security features enabled\n')

    print(
        f'curl -s -XPOST \'http://{conf.elastic_url_port}/_bulk\' --data-binary @{conf.output_dir}/{conf.app_output_file}-{filedate}.json -H \"Content-Type: application/x-ndjson\" \n')


if __name__ == '__main__':
    metrics_apps()