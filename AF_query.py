#!/usr/bin/env python3
import sys
import os
import os.path
import json
import time

from panafapi_hacked import panafapi_hacked

def main():

    libpath = os.path.dirname(os.path.abspath(__file__))
    sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
    thismodule = sys.modules[__name__]

    print(time.strftime("%d/%m/%Y"))

# initialize xml variable dictionary

    tag_response = {}
    domain = []
    api_key = '7fac67a8-6022-4693-9298-e36cab3d8192'
    hostname = 'autofocus.paloaltonetworks.com'

# read the domain list file - a simple text list of malicious or suspect domains
# the text file is converted to a simple python list

    with open('domain_list.txt','r') as domainFile:
        domain = domainFile.read().splitlines()


# query domain to get tags

    tag_dict = {}
    domains_and_tags = {}

    for dns_domain in domain:
        print('\nworking with domain = {0}\n'.format(dns_domain))
        domains_and_tags[dns_domain] = {}
        domains_and_tags[dns_domain]['malware'] = []
        af_output = panafapi_hacked(hostname, api_key, 'get_tags', dns_domain, False)

# domain_dict is the response from the Autofocus domain query
# json converted to python dictionary

        domain_dict = json.loads(af_output)

        for item in domain_dict['hits']:
            record = item['_source']
            for item in record:

# parsing the response to find the tag information
# then when required, creating a new tag dictionary entry for newly found tags

                af_tags = record['tag']
                for item in af_tags:
                    if item in tag_dict:
                        pass
                    else:

# for new tags do a secondary query to get the tag type aka the 'tag class' in Autofocus
# this captures all tag responses in the local tag dictionary

                        tag_types = get_tags(hostname, api_key, 'tag_info', False, item)
                        tags_dict = json.loads(tag_types)
                        tag_dict[item] = {}
                        tag_dict[item]['class'] = tags_dict['tag']['tag_class']


                        if not tags_dict['tag_groups']:
                            pass
                        else:                      
                            tag_dict[item]['group'] = tags_dict['tag_groups'][0]['tag_group_name']

                            # Append tag file with new tag data
                        with open('tag_data.txt','w') as tagFile:
                            tagFile.write(json.dumps(tag_dict, indent=4, sort_keys=True))

# the application is looking for tags related to a named malware family
# If a match then the domain list dictionary is updated with the malware family
                    
                    if tag_dict[item]['class'] == 'malware_family':
                      if item in domains_and_tags[dns_domain]['malware']:
                          pass
                      else:
                        domains_and_tags[dns_domain]['malware'].append(item)
        print('\n' + json.dumps(domains_and_tags[dns_domain], indent=4))

# write tag and domain data to text file

        with open('domain_tags.txt','w') as domainFile:
                domainFile.write(json.dumps(domains_and_tags, indent=4, sort_keys=True))


# after completing queries for the domain list show the summary output of domain and tag information

    print('\nThe domain and tag dictionary with a malware family where applicable:\n')
    print(json.dumps(domains_and_tags, indent=4, sort_keys=True))
    print('\n\nThe query reply tag dictionary including class and group:\n')
    print(json.dumps(tag_dict, indent=4, sort_keys=True))
    print('\n')


if __name__ == '__main__':
    main()






            
