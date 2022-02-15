# Parse Threat Data Tools
Parse threat data sheets into estack loadable output


### Data loads

Data categories and indexes for daily counts include:

    * daily sample counts by file type for all/malware verdicts, all/customer sources
    * daily application counts across all sessions
    * daily signature counts by file type

Indexes are appended with the year-month created date-based groupings.

### python metrics files

    * metrics_apps: read and reformat daily appliation counts
    * metrics_samples: read and combine the (4) input sample files then format out to json
    * metrics_sigs: read and reformat daily sig counts
    * name_mapping_apps: rename and reformat output apps csv file from kibana
    * name_mapping_samples: rename and reformat output samples csv file from kibana
    * name_mapping_sigs: rename and reformat output sigs csv file from kibana

### conf.py file

this file is used for basic config settings and file type data enhancements associated to
the python files.

#### filetype dicts

In conf.py are two dicts: filetypetags and sigfiletypetags. These are used to map the
raw filenames in the sample and sig data to both a `group` to simplify the output view names
and `autofocus` to associate to Autofocus filetype names.


### Loading into Elasticsearch

Output json files are designed to be bulk loaded into Elasticsearch.
The metrics files will print the curl command specific to the data run to copy-paste.

Add new data to the index with dir/filename after `@`

```
   curl -s -XPOST 'http://localhost:9200/_bulk' --data-binary @metrics_threat_output/metrics_threat_apps-2020-05-08T09-39-01Z.json -H "Content-Type: application/x-ndjson"
```

> loading may require appending `-u username:password` if security features enabled

> if adding new fields be sure to update the index pattern in Kibana


Delete existing data in the index by index or using wildcards

```
   curl -XDELETE http://localhost:9200/metrics-threat-samples-2020-04
```

## Imported to ELK incorrectly?

- Delete a range of dates:
```
POST <index>/_delete_by_query
{
  "query": {
    "range" : {
        "date" : {
           "gte" : "YYYY-MM-DD",
           "lte" : "YYYY-MM-DD"
        }
    }
  }
}
```
- Delete a single date:
```
POST <index>/_delete_by_query
{
  "query": {
      "term" : {"date" : "YYYY-MM-DD>T00:00:00.000"}
  }
}
```




