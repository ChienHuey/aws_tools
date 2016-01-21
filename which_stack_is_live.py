# Script to show which CloudFormation stack is active for a given property
#
# python which_stack_is_live.py <aws_cli profile name> <property name in Fastly> <Fastly api key>
#
# @param    aws_cli profile name
# @param    property name in Fastly
# @param    Fastly API key

import boto3
import fastly
import sys

__author__ = 'chhuey'

if len(sys.argv) != 4:
    print "usage which_stack_is_live <aws_cli profile name> <property name in Fastly> <Fastly API key>"
    sys.exit(0)
else:
    fastlyAPIKey = sys.argv[3]
    awscliProfile = sys.argv[1]
    propertyName = sys.argv[2]


awsSession = boto3.session.Session(awscliProfile)

client = fastly.connect(fastlyAPIKey)
propertyShareId = ''
lastVersion = 0

# get all the services on Fastly
allServices = client.list_services()

# determine the Fastly shareID of the property
service = client.get_service_by_name(propertyName)
versionList = service._data['versions']
lastVersion = int(versionList[-1]['number'])
propertyShareId = versionList[-1]['service']


