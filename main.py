#!/usr/bin/python3

import sys
import configparser
import json
import os

from os.path import expanduser

if(len(sys.argv) <= 1):
    exit("Need named profile")


home = expanduser("~")
requestedProfile = sys.argv[1]
awsConfig = configparser.ConfigParser()
awsCred = configparser.ConfigParser()

awsConfig.read("%s/.aws/config" % home)
awsCred.read("%s/.aws/credentials" % home)

print(awsConfig)

try:
    mfaARN = awsConfig[awsConfig["profile " + requestedProfile]['source_profile']]['mfa_serial']
except KeyError:
    try:
        mfaARN = awsConfig['default']['mfa_serial']
    except KeyError:
        exit("Need MFA serial in config file")

configProfiles = set(awsConfig.sections())
profiles = set(awsCred.sections())

if(requestedProfile in profiles and "profile " + requestedProfile in configProfiles):
    print("Updating %s profile" % requestedProfile)
else:
    if("profile " + requestedProfile in configProfiles):
        print("Creating %s credentials profile" % requestedProfile)
        awsCred.add_section(requestedProfile)
    else:
        exit("No Such Profile \"$s\" in config" % requestedProfile)

try:
    OneTimeNumber = int(input("OTP from device: "))
except ValueError:
    exit("OTP must be a number")

response = os.popen("aws --profile %s sts get-session-token --serial-number %s --token-code %s"
                    % (awsConfig["profile " + requestedProfile]['source_profile'],
                      mfaARN,
                      str(OneTimeNumber).zfill(6))).read()

print(response)

try:
    myjson = json.loads(response)
except json.decoder.JSONDecodeError:
    exit("Decode Fail")

awsCred[requestedProfile]['aws_access_key_id'] = myjson['Credentials']['AccessKeyId']
awsCred[requestedProfile]['aws_secret_access_key'] = myjson['Credentials']['SecretAccessKey']
awsCred[requestedProfile]['aws_session_token'] = myjson['Credentials']['SessionToken']

with open("%s/.aws/credentials" % home, 'w') as awsCredFile:
    awsCred.write(awsCredFile)

