####!/usr/bin/env python3
"""
Parse data files with json output for estack bulk load
"""

# from lxml import etree
import xml.etree.ElementTree as etree
import json

def appxml_parse():

    """
    daily sample counts for all verdicts and malware verdict

    """

# open and read in the app data
    tree = etree.parse('appdata.xml')
    root = tree.getroot()

    apptags = {}

    for app in root.getchildren():

        appname = app.attrib['name']
        apptags[appname] = {}
        if app.find("./subcategory") is not None:
            apptags[appname]['subcategory'] = app.find("./subcategory").text
        else:
            apptags[appname]['subcategory'] = 'tag_unknown'

        if app.find("./is-saas") is not None:
            apptags[appname]['is-saas'] = app.find("./is-saas").text
        else:
            apptags[appname]['is-saas'] = 'tag_unknown'

#    print(apptags)

    with open('apptags.json', 'w') as f:
        f.write(json.dumps(apptags, indent=2, sort_keys=False))


if __name__ == '__main__':
    appxml_parse()