####!/usr/bin/env python3
"""
Parse data files with json output for estack bulk load
"""

import datetime
import json
from xlrd import open_workbook
from conf import samples_output, samples_source, samples_sheetname, malware_source, malware_sheetname, sample_elkindex
from tagdata.elk_index import elk_index


def dailycounts():

    """
    daily sample counts for all verdicts and malware verdict

    """

# open and read in the all samples data
    allsamples = open_workbook(samples_source)
    allsheet = allsamples.sheet_by_name(samples_sheetname)

# open and read in the malware samples data
    malsamples = open_workbook(malware_source)
    malsheet = malsamples.sheet_by_name(malware_sheetname)

    sample_data_dict = {}

    with open(samples_output, 'w') as f:
        print('flush to rebuild the sample count file')

    for row in range(2, allsheet.nrows):

        timestamp = allsheet.cell(row,0).value
        sample_data_dict['date'] = str((datetime.datetime.strptime(timestamp, " %Y-%m-%d %H:%M:%S ")).date())
        sample_data_dict['totalcount'] = int(allsheet.cell(row,1).value)
        sample_data_dict['malcount'] = int(malsheet.cell(row, 1).value)

        index_tag_full = elk_index(sample_elkindex)

        with open(samples_output, 'a') as file:
            file.write(json.dumps(index_tag_full, indent=None, sort_keys=False) + "\n")
            file.write(json.dumps(sample_data_dict, indent=None, sort_keys=False) + "\n")

    return

if __name__ == '__main__':
    dailycounts()