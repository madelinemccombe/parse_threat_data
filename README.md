# Threat Data Parse Tools
Parse threat data sheets into estack loadable output


## Data loads

Data categories and indexes for daily counts include:

* counts for all verdicts and malware
* malware by filetype and upload source
* malware by application
* AV/Wildfire signatures
* AV/Wildfire sigs and related filetypes
* Top 20 Sig-Sample ratios


## Loading into Elasticsearch

Output json are designed to be bulk loaded into Elasticsearch


## INSTALLATION

###### 1. Clone repo
git clone https://github.com/scotchoaf/parse_threat_data.git

###### 2. Create python 3.6 virtualenv
```
$ python3.6 -m venv env
```

###### 3. Active virtualenv
```
$ source env/bin/activate
```

###### 4. Change into repo directory
```
$ cd parse_threat_data
```

###### 5. Download required libraries
```
$ pip install -r requirements.txt
```

###### 6. Enter or validate values in the conf.py file
```
$ vi conf.py --> **Or editor of choice**
```

###### 7. Run the python file specific to data to parse
```
$ python samplecounts.py

$ python filetypecounts.py

$ python appcounts.py

$ python sigfiletypecounts.py
```

###### 8. Output in the estackfiles folder ready for bulk loading

Instructions for elasticsearch bulk load per output in the docs folder. Format:

```
$ curl -s -XPOST 'http://localhost:9200/_bulk' --data-binary @samplecounts.json -H "Content-Type: application/x-ndjson"
```

