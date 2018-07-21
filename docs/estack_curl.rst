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
   curl -XDELETE http://localhost:9200/samplecounts

Add new data to the index

::
   curl -s -XPOST 'http://localhost:9200/_bulk' --data-binary @samplecounts.json -H "Content-Type: application/x-ndjson"


Filetype counts
---------------

Full daily sample counts broken down by filetype information

.. highlight:: bash

Delete existing data in the index

::
   curl -XDELETE http://localhost:9200/filecounts

Add new data to the index

::
   curl -s -XPOST 'http://localhost:9200/_bulk' --data-binary @sfilecounts.json -H "Content-Type: application/x-ndjson"


