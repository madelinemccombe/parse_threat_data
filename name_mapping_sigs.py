#!/usr/bin/env python3
# Copyright (c) 2018, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Authors: Scott Shoaf

import json
import csv
from datetime import datetime

import click

@click.command()
@click.option("-f", "--filename", help="file name", type=str, default='')
def cli(filename):
    """
    grab github traffic stats and generate csv output
    :param git_token: personal auth token used for API access
    :param filenamme: csv list of orgs and repos
    :return: None
    """

    # timestamp to be added to the file name
    filedate = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
    output_filename = 'metrics_threat_output/metrics_threat_sigs'
    skip_fields = ['_id','_index','_score','_type', 'date']
    int_fields = [
        "metrics.threat.signatures.count"
        ]

    # create empty json output files
    with open(f'{output_filename}-{filedate}.json', 'w') as f:
        print(f'writing to file: {output_filename}-{filedate}.json')

    # get csv data and format to bulk load json
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_dict = {}
            date_datetime = datetime.strptime(row['date'], '%b %d, %Y @ %H:%M:%S.%f')
            kibana_date = date_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
            data_dict['date'] = str(kibana_date)
            for key in row:
                if key not in skip_fields:
                    if key in int_fields:
                        try:
                            if row[key] is not None:
                                row[key] = int(float(str(row[key]).replace(",", "")))
                                data_dict[key] = row[key]
                            else:
                                data_dict[key] = int(0.0)
                        except:
                            data_dict[key] = int(0.0)

                    else:
                        data_dict[key] = row[key]

            index_tag_full = {}
            index_tag_inner = {}
            elk_index_name = f"metrics-threat-signatures-{date_datetime.year}-{date_datetime.strftime('%m')}"
            index_tag_inner['_index'] = f'{elk_index_name}'
            index_tag_inner['_type'] = f'{elk_index_name}'
            index_tag_full['index'] = index_tag_inner

            with open(f'{output_filename}-{filedate}.json', 'a') as f:
                f.write(json.dumps(index_tag_full, indent=None, sort_keys=False) + "\n")
                f.write(json.dumps(data_dict, indent=None, sort_keys=False) + "\n")


if __name__ == '__main__':
    cli()
