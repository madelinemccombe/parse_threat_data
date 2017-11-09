# Safe Network Tools
Demo Safenetworking configuration creator and Autofocus domain-tag validation queries

These apps are used to complement the SafeNetwork application

## Autofocus Domain queries

Useful to check a list of domain values to determine if tags, especially of class 'malware_family' exists in Autofocus.

## Firewall configuration utility

Provides a set of templates with input variables. The user can either create config snippets to manually load into the firewall or leverage the firewall API to quickly configuration and commit the Safe Networking required configuration.

## INSTALLATION

###### 1. Clone repo
git clone https://github.com/scotchoaf/safeNetwork_tools.git

###### 2. Create python 3.6 virtualenv 
$ python3.6 -m venv env

###### 3. Active virtualenv
$ source env/bin/activate

###### 4. Change into repo directory
$ cd safeNetwork_tools

###### 5. Download required libraries
$ pip install -r requirements.txt


## Using the Autofocus Query tool

###### 1. Edit the domain_list.txt file with a set of domains to query
NOTE: This is a simple input list using linebreaks and not a CSV format

###### 2. Edit the API key value in the domain_tag.py file
This is the Autofocus API key used for api interactions
NOTE: Check the daily quota value to ensure enough points to run queries

###### 3. Run the python application
$ python ./domain_tag.py

###### 4. Monitor and check final results
The output per domain and end-of-run summary will appear in the output window
When complete two files are created:
* the domain_tags.txt file shows json output of all domains and associated malware family tags 
* the tag_data.txt file with all tag values returned and associated class and group values


## Using the Firewall configuration utility

###### 1. Edit the variable values in input-var.csv
Set CONFIG_API:NO to only creates files or CONFIG_API:YES to send configs using the api

###### 2. Run the python configuration file
$ python ./configxml.py 

###### 3. Enter the api user and password when prompted
* Make sure there is connectivity to the device
* Validate that the user account has API write permissions

###### 4. Output files will be stored in xml-templates
The folder name is based on the csv Customer name and firewall IP values
