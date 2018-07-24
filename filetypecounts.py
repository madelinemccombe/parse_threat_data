####!/usr/bin/env python3
"""
Parse data files with json output for estack bulk load
"""

import datetime
import xlrd
import json
from xlrd import open_workbook
from conf import filetypes_output, filetypes_sheetname, filetypes_source, filetype_elkindex
from tagdata.elk_index import elk_index
from tagdata.datatags import filetypetags


def filetypecounts():

    """
    filetype daily counters for malware verdict samples

    """

# open and read in the all samples data
    filesamples = open_workbook(filetypes_source)
    filesheet = filesamples.sheet_by_name(filetypes_sheetname)

    filetype_data_dict = {}

    with open(filetypes_output, 'w') as f:
        print('flush to rebuild the filetype count file')

    for row in range(2, filesheet.nrows):
        timestamp = datetime.datetime(*xlrd.xldate_as_tuple(filesheet.cell(row, 0).value, filesamples.datemode))
        filetype_data_dict['date'] = str(timestamp.date())
        filetype_data_dict['filetype'] = filesheet.cell(row, 1).value
        filetype_data_dict['count'] = int(filesheet.cell(row,2).value)

        filetype = filetype_data_dict['filetype']
        filetype_data_dict['filegroup'] = filetypetags[filetype][0]
        filetype_data_dict['afname'] = filetypetags[filetype][1]

        index_tag_full = elk_index(filetype_elkindex)

        with open(filetypes_output, 'a') as file:
            file.write(json.dumps(index_tag_full, indent=None, sort_keys=False) + "\n")
            file.write(json.dumps(filetype_data_dict, indent=None, sort_keys=False) + "\n")

    return


if __name__ == '__main__':
    filetypecounts()