####!/usr/bin/env python3
"""
Parse data files with json output for estack bulk load
"""

import datetime
import xlrd
import json
from xlrd import open_workbook
from conf import app_output, app_sheetname, app_source, app_elkindex
from lib.elk_index import elk_index
from lib.datatags import filetypetags


def appcounts():

    """
    sample application source daily counters for malware verdict samples

    """

# open and read in the all samples data
    filesamples = open_workbook(app_source)
    filesheet = filesamples.sheet_by_name(app_sheetname)

    filetype_data_dict = {}

    with open(app_output, 'w') as f:
        print('flush to rebuild the filetype count file')

    for row in range(2, filesheet.nrows):
        timestamp = datetime.datetime(*xlrd.xldate_as_tuple(filesheet.cell(row, 0).value, filesamples.datemode))
        filetype_data_dict['date'] = str(timestamp.date())
        filetype_data_dict['application'] = filesheet.cell(row, 1).value
        filetype_data_dict['count'] = int(filesheet.cell(row,2).value)

# Add in application group if needed
#        filetype = filetype_data_dict['filetype']
#        filetype_data_dict['filegroup'] = filetypetags[filetype][0]
#        filetype_data_dict['afname'] = filetypetags[filetype][1]

        index_tag_full = elk_index(app_elkindex)

        with open(app_output, 'a') as file:
            file.write(json.dumps(index_tag_full, indent=None, sort_keys=False) + "\n")
            file.write(json.dumps(filetype_data_dict, indent=None, sort_keys=False) + "\n")

    return


if __name__ == '__main__':
    appcounts()