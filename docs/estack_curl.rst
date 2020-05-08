Threat Data Parse
=================

Parse threat data xlsx files and prep for ElasticSearch bulk load

Each curl is to delete and then add new data to the index.


Sample counts
-------------

Full daily sample counts

.. highlight:: bash

Delete existing data in the index

::
   curl -XDELETE http://localhost:9200/metrics-threat-samples-2020-04

Add new data to the index

::
   curl -s -XPOST 'http://localhost:9200/_bulk' --data-binary @metrics_threat_output/metrics_threat_apps-2020-05-08T09-39-01Z.json -H "Content-Type: application/x-ndjson"


Filetype counts
---------------

Full daily sample counts broken down by filetype information

.. highlight:: bash

Delete existing data in the index

::
   curl -XDELETE http://localhost:9200/filecount

Add new data to the index

::
   curl -s -XPOST 'http://localhost:9200/_bulk' --data-binary @filecounts.json -H "Content-Type: application/x-ndjson"


Sigfiletype counts
---------------

Full daily sample counts broken down by filetype information

.. highlight:: bash

Delete existing data in the index

::
   curl -XDELETE http://localhost:9200/sigfiletypecounts

Add new data to the index

::
   curl -s -XPOST 'http://localhost:9200/_bulk' --data-binary @sigcounts.json -H "Content-Type: application/x-ndjson"


Sample application counts
-------------------------

Full daily sample counts broken down by session application

.. highlight:: bash

Delete existing data in the index

::
   curl -XDELETE http://localhost:9200/appcounts

Add new data to the index

::
   curl -s -XPOST 'http://localhost:9200/_bulk' --data-binary @appcounts.json -H "Content-Type: application/x-ndjson"




