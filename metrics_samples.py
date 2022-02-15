####!/usr/bin/env python3
"""
Parse data files with json output for estack bulk load
"""

import json
import sys
from datetime import datetime, timedelta

from xlrd import open_workbook

import conf


def metrics_samples():
    """
    filetype daily counters for malware verdict samples

    """

    # create list of filetypes to check for new additions
    filetype_list = []

    # grab all input data and write into a master dict
    raw_data = {}

    for datatype in conf.input_file_data:
        input_file = open_workbook(f'{conf.input_dir}/{conf.input_file_data[datatype][0]}')
        input_sheet = input_file.sheet_by_name(conf.input_file_data[datatype][1])
        raw_data[datatype] = {}

        for row in range(2, input_sheet.nrows):
            row_date = input_sheet.cell(row, 0).value
            file_type = input_sheet.cell(row, 1).value
            file_count = int(input_sheet.cell(row, 2).value)

            if row_date in raw_data[datatype]:
                pass
            else:
                raw_data[datatype][row_date] = {}

            raw_data[datatype][row_date][file_type] = file_count

            # generate list of all filetypes
            if file_type in filetype_list:
                pass
            else:
                filetype_list.append(input_sheet.cell(row, 1).value)

    # check that all filetypes are captured
    # if any are missing stop and user has to update the file list in conf.py
    missing_filetypes = []
    for filetype in filetype_list:
        if filetype in conf.filetypetags:
            pass
        else:
            missing_filetypes.append(filetype)

    if len(missing_filetypes) > 0:
        print('found missing filetypes')
        print(missing_filetypes)
        sys.exit()

    # timestamp to be added to the file name
    filedate = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')

    # create empty json output file
    with open(f'{conf.output_dir}/{conf.output_filename}-{filedate}.json', 'w') as f:
        print(f'writing to file: {conf.output_dir}/{conf.output_filename}-{filedate}.json')

    # set start date for appending the data set
    start_date = datetime.strptime(conf.start_date, '%Y-%m-%d')
    stop_date = datetime.strptime(conf.stop_date, '%Y-%m-%d')
    item_date = start_date

    # generate daily stats and write to dict for csv output
    while item_date <= stop_date:

        # first formats the date for elasticsearch and second to search input values
        raw_date = item_date.strftime('%Y-%m-%d')
        # print(raw_date)
        for filetype in filetype_list:
            stats_dict = {}
            stats_dict['date'] = item_date.strftime('%Y-%m-%dT00:00:00Z')
            stats_dict['metrics.threat.samples.filetype.raw'] = filetype
            stats_dict['metrics.threat.samples.filetype.group'] = conf.filetypetags[filetype][0]
            stats_dict['metrics.threat.samples.filetype.autofocus'] = conf.filetypetags[filetype][1]

            # check raw_dict and add counts if exist or set to zero
            # get counts for all verdicts and all sources
            if filetype in raw_data['verdict_all_all'][raw_date]:
                stats_dict['metrics.threat.samples.verdict.all.all'] = raw_data['verdict_all_all'][raw_date][filetype]
            else:
                stats_dict['metrics.threat.samples.verdict.all.all'] = 0

            # get counts for all verdicts and customer source
            if filetype in raw_data['verdict_all_NO245'][raw_date]:
                stats_dict['metrics.threat.samples.verdict.all.customer'] = raw_data['verdict_all_NO245'][raw_date][
                    filetype]
            else:
                stats_dict['metrics.threat.samples.verdict.all.customer'] = 0

            # get counts for all verdicts and all sources
            if filetype in raw_data['verdict_mal_all'][raw_date]:
                stats_dict['metrics.threat.samples.verdict.malware.all'] = raw_data['verdict_mal_all'][raw_date][
                    filetype]
            else:
                stats_dict['metrics.threat.samples.verdict.malware.all'] = 0

            # get counts for all verdicts and customer source
            if filetype in raw_data['verdict_mal_NO245'][raw_date]:
                stats_dict['metrics.threat.samples.verdict.malware.customer'] = raw_data['verdict_mal_NO245'][raw_date][
                    filetype]
            else:
                stats_dict['metrics.threat.samples.verdict.malware.customer'] = 0

            # calculate toxicity ratio comparing malware vs all verdicts - customer source
            if filetype in raw_data['verdict_all_NO245'][raw_date] and filetype in raw_data['verdict_mal_NO245'][
                raw_date]:
                stats_dict['metrics.threat.samples.toxicity.customer'] = raw_data['verdict_mal_NO245'][raw_date][
                                                                             filetype] / \
                                                                         raw_data['verdict_all_NO245'][raw_date][
                                                                             filetype]

            # calculate toxicity ratio comparing malware vs all verdicts - all sources
            if filetype in raw_data['verdict_all_all'][raw_date] and filetype in raw_data['verdict_mal_all'][raw_date]:
                stats_dict['metrics.threat.samples.toxicity.all'] = raw_data['verdict_mal_all'][raw_date][filetype] / \
                                                                    raw_data['verdict_all_all'][raw_date][filetype]

            # calculate feed counts for all verdicts as diff of all and customer sources
            stats_dict['metrics.threat.samples.verdict.all.feed'] = \
                stats_dict['metrics.threat.samples.verdict.all.all'] - \
                stats_dict['metrics.threat.samples.verdict.all.customer']

            # calculate feed counts for malware verdicts as diff of all and customer sources
            stats_dict['metrics.threat.samples.verdict.malware.feed'] = \
                stats_dict['metrics.threat.samples.verdict.malware.all'] - \
                stats_dict['metrics.threat.samples.verdict.malware.customer']

            # create elk index by month and year
            index_tag_full = {}
            index_tag_inner = {}
            elk_index_name = f"threat-samples-{item_date.year}-{item_date.strftime('%m')}"
            index_tag_inner['_index'] = f'{elk_index_name}'
            index_tag_inner['_type'] = '_doc'
            index_tag_full['index'] = index_tag_inner

            with open(f'{conf.output_dir}/{conf.output_filename}-{filedate}.json', 'a') as file:
                file.write(json.dumps(index_tag_full, indent=None, sort_keys=False) + "\n")
                file.write(json.dumps(stats_dict, indent=None, sort_keys=False) + "\n")

        item_date = item_date + timedelta(days=1)

    # print out the elasticSearch bulk load curl commands
    print('\nUse curl -XDELETE [url]:[port]/index to delete data from the index')
    print('use the XPOST curl command to load json data to elasticSearch')
    print('add -u with username:password if security features enabled\n')

    print(
        f'curl -s -XPOST \'http://{conf.elastic_url_port}/_bulk\' --data-binary @{conf.output_dir}/{conf.output_filename}-{filedate}.json -H \"Content-Type: application/x-ndjson\" \n')


if __name__ == '__main__':
    metrics_samples()
