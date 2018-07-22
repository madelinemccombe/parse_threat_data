####!/usr/bin/env python3
"""
Parse data files with json output for estack bulk load
"""

import datetime
import xlrd
import json
from xlrd import open_workbook
from conf import sigfiletypes_output, sigfiletypes_sheetname, sigfiletypes_source, sigfiletype_elkindex
from lib.elk_index import elk_index
from lib.datatags import sigfiletypetags


def sigfiletypecounts():

    """
    Sig and filetype daily counters for daily sig releases

    """

# open and read in the all samples data
    filesamples = open_workbook(sigfiletypes_source)
    filesheet = filesamples.sheet_by_name(sigfiletypes_sheetname)

    filetype_data_dict = {}

    with open(sigfiletypes_output, 'w') as f:
        print('flush to rebuild the filetype count file')

    for row in range(2, filesheet.nrows):
        timestamp = datetime.datetime(*xlrd.xldate_as_tuple(filesheet.cell(row, 0).value, filesamples.datemode))
        filetype_data_dict['date'] = str(timestamp.date())
        filetype_data_dict['filetype'] = filesheet.cell(row, 1).value
        filetype_data_dict['count'] = int(filesheet.cell(row,2).value)

        filetype = filetype_data_dict['filetype']
        filetype_data_dict['filegroup'] = sigfiletypetags[filetype][0]
        filetype_data_dict['afname'] = sigfiletypetags[filetype][1]

        index_tag_full = elk_index(sigfiletype_elkindex)

        with open(sigfiletypes_output, 'a') as file:
            file.write(json.dumps(index_tag_full, indent=None, sort_keys=False) + "\n")
            file.write(json.dumps(filetype_data_dict, indent=None, sort_keys=False) + "\n")

    return


if __name__ == '__main__':
    sigfiletypecounts()