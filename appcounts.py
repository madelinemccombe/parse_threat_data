####!/usr/bin/env python3
"""
Parse data files with json output for estack bulk load
"""

import datetime
import xlrd
import json
from xlrd import open_workbook
from conf import app_output, app_sheetname, app_source, app_elkindex
from tagdata.elk_index import elk_index


def appcounts():

    """
    sample application source daily counters for malware verdict samples

    """

# open and read in the all samples data
    filesamples = open_workbook(app_source)
    filesheet = filesamples.sheet_by_name(app_sheetname)

    app_data_dict = {}

    with open(app_output, 'w') as f:
        print('flush to rebuild the application count file')

    with open('tagdata/apptags.json', 'r') as tagfile:
        apptags = json.load(tagfile)

    for row in range(2, filesheet.nrows):
        timestamp = datetime.datetime(*xlrd.xldate_as_tuple(filesheet.cell(row, 0).value, filesamples.datemode))
        app_data_dict['date'] = str(timestamp.date())
        app_data_dict['application'] = filesheet.cell(row, 1).value
        app_data_dict['count'] = int(filesheet.cell(row,2).value)

        # Add in application tags from tagdata/apptags.json
        # tag with app_unknown if data app not in applipedia
        appname = app_data_dict['application']

        if appname in apptags:
            app_data_dict['subcategory'] = apptags[appname]['subcategory']
            app_data_dict['is-saas'] = apptags[appname]['is-saas']
        else:
            app_data_dict['subcategory'] = 'app_unknown'
            app_data_dict['is-saas'] = 'app_unknown'

        index_tag_full = elk_index(app_elkindex)

        with open(app_output, 'a') as file:
            file.write(json.dumps(index_tag_full, indent=None, sort_keys=False) + "\n")
            file.write(json.dumps(app_data_dict, indent=None, sort_keys=False) + "\n")

    return


if __name__ == '__main__':
    appcounts()