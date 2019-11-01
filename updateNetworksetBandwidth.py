###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###
##  Nov 2019 - v1.0
##      Use REST API to OneView
##      - Initial call to get Session ID
##      - Use Session ID for GET , POST, PUT instead of username, password
##  Main function:
##      Update bandwidth for network set 

from pprint import pprint
import json
import copy
import csv
import requests
import os
from os import sys


from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TABSPACE        = "    "
COMMA           = ','
CR              = '\n'
CRLF            = '\r\n'




# Connect to new OneView instance to collect interconnect types information
print(CR)
print('#---------------- Connect to Oneview instance')
config_file = '/oneview_config.json'   
with open(config_file) as json_data:
    config = json.load(json_data)
oneview_client = OneViewClient(config)


# Get OneView credentials for REST API calls
ovIP                    = config['ip']
ovAPI                   = config['api_version']
ovUser                  = config['credentials']['userName']
ovPassword              = config['credentials']['password']

cred  = dict()
cred.update(userName = '{}'.format(ovUser))
cred.update(password   = '{}'.format(ovPassword))

# POST REST to get sesion ID
auth_uri            = 'https://{}/rest/login-sessions'.format(ovIP)
headers             = {
    'content-type': 'application/json',
    'X-Api-Version':'{0}'.format(ovAPI)  
    }
resp = requests.post(auth_uri, headers=headers, timeout=60, verify=False,data=json.dumps(cred))

# Format the response to extract sessionID
token       = json.loads(resp.text)
sessionID   = token['sessionID']

# Add session ID to headers
headers.update(Auth = '{}'.format(sessionID))

# Get all connection templates
urn = "https://{0}/{1}".format(ovIP,'/rest/connection-templates/')
resp = requests.get(urn, headers=headers, timeout=60, verify=False) 
data = json.loads(resp.text)

connection_templates = data['members']


#### Read CSV files
print(CR)
print('#---------------- Read CSV file to get network set and its bandwidth')

csvFile     = networkset.csv'
with open(csvFile, 'r') as f:                                     
    reader = csv.DictReader(f)
    for row in reader:
        nsName                  = row["name"]
        typicalBandwidth        = row['typicalBandwidth']
        maximumBandwidth        = row['maximumBandwidth']

        ns                      = oneview_client.network_sets.get_by('name', nsName)[0]

        if ns:              
            con_template_uri    = ns['connectionTemplateUri']
            this_con_template   = None
            for connection in connection_templates:
                if con_template_uri in connection['uri']:
                    this_con_template = connection

            if this_con_template:
                print(CR)
                print('#---------------- Update networkset {0} with typicalbandwidth {1} and maximumbandwidth {2}'.format(nsName,typicalBandwidth,maximumBandwidth))
                # Found the connection template associated to network set
                # UPdate bandwidth 
                this_con_template['bandwidth'].update(maximumBandwidth   = '{}'.format(maximumBandwidth))
                this_con_template['bandwidth'].update(typicalBandwidth   = '{}'.format(typicalBandwidth))

                con_template_uri = "https://{0}".format(ovIP) + con_template_uri

                # Update associated connection template with new bandwdith values
                resp = requests.put(con_template_uri, data = json.dumps(this_con_template), headers=headers, timeout=60, verify=False)

                print('returned status --> ', resp)

