Threat Data Parse
=================

Parse threat data xlsx files and prep for ElasticSearch bulk load

Each curl is to delete and then add new data to the index.


Bulk deletes and loading
------------------------

Full daily sample counts

.. highlight:: bash

Delete existing data in the index

::
   curl -XDELETE http://localhost:9200/metrics-threat-signatures-2020-01

Add new data to the index

::
   curl -s -XPOST 'http://localhost:9200/_bulk' --data-binary @metrics_threat_output/metrics_threat_sigs-2020-05-13T10-57-06Z.json -H "Content-Type: application/x-ndjson"







