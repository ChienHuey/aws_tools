# Script to show which CloudFormation stack is active for a given property
#
# python which_stack_is_live.py <aws_cli profile name> <property name in Fastly> <Fastly api key>
#
# @param    aws_cli profile name
# @param    property name in Fastly
# @param    Fastly API key
# @param    Fastly username (optional)
# @param    Fastly password (optional)

import boto3
import fastly
import re
import sys

__author__ = 'chhuey'

def get_active_version(versions):
    active_version_number = 0
    index = len(versions) - 1
    while index >= 0:
        if versions[index]['active'] == '1':
            active_version_number = int(versions[index]['number'])
            break
        else:
            index -= 1
    return active_version_number

def parse_vcl(active_version):
    vcl_list = active_version['vcl']
    backend_vcl = ""
    # find the vcl with backend information
    for vcl in vcl_list:
        if re.match('backend', vcl['content']):
            backend_vcl = vcl['content']
            break

    print backend_vcl


if len(sys.argv) < 4:
    print "usage which_stack_is_live <aws_cli profile name> <property name in Fastly> <Fastly API key>"
    sys.exit(0)
else:
    fastlyAPIKey = sys.argv[3]
    awscliProfile = sys.argv[1]
    propertyName = sys.argv[2]
    fastlyUserId = sys.argv[4]
    fastlyPassword = sys.argv[5]


awsSession = boto3.session.Session(awscliProfile)

client = fastly.connect(fastlyAPIKey)
client.login(fastlyUserId, fastlyPassword)
propertyshareid = ""
lastVersion = 0

# determine the Fastly shareID of the property
service = client.get_service_by_name(propertyName)
versionList = service._data['versions']
activeVersion = get_active_version(versionList)
propertyshareid = versionList[-1]['service']

# list all the backends associated with the service
backends = client.list_backends(propertyshareid, activeVersion)

if len(backends) == 0:
    version_to_go = activeVersion - 1
    active_version = versionList[version_to_go]
    parse_vcl(active_version)







