# pip install twilio
# pip install python-dotenv

import os
from os.path import join, dirname
from dotenv import load_dotenv
import csv
import time
from shutil import copyfile
import requests
import sys, base64, datetime, hashlib, hmac 
import json
import boto3

client = boto3.client('pinpoint')

host="pinpoint.us-east-1.amazonaws.com"
region="us-east-1"
serviceName = "mobiletargeting"
pintPointEndpoint = "https://pinpoint.us-east-1.amazonaws.com/v1/phone/number/validate"
ts = str(time.time())

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

accessKey = os.environ.get('AWS_ACCESS_KEY_ID')
secretAccessKey = os.environ.get('AWS_SECRET_ACCESS_KEY')

def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

def writeCsv(file_name, row):
    with open(file_name, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter =',')
        writer.writerow(row)

def overWriteCsv(file_name, data):
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter =',')
        for row in data:
            writer.writerow(row)

def readCsv(filename):
    result = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            result.append(row)

    return result

def lookUp(number):
    response = client.phone_number_validate(
        NumberValidateRequest={
            'IsoCountryCode': 'US',
            'PhoneNumber': number
        }
    )
    phoneType = response['NumberValidateResponse']['PhoneType']
    # print(response['NumberValidateResponse'])
    
    return phoneType

def bulkLookup(filename):
    copyfile('./input/' + filename, './input/' + filename.split('.')[0] + '-origin' + '.csv')
    allContacts = readCsv('./input/' + filename)
    counter = 1

    if len(allContacts) <= 1:
        print('Nothing to lookup')
    else:
        for index, contact in enumerate(allContacts[1:len(allContacts)]):
            number = contact[2]

            try:
                type = lookUp(number).lower()
                print('[Counter]', counter)
                print('[Total index]', index + 1)
                print('[Type]', type)

                if type == 'mobile' or type == 'voip':
                    writeCsv('./output/' + filename.split('.')[0] + '-' + ts + '.csv', contact)
                    overWriteCsv('./input/' + filename, allContacts[index + 1:len(allContacts)])

                if counter >= 500:
                    time.sleep(5)
                    counter = 1

                counter = counter + 1
            except:
                continue

if __name__ == '__main__':
    t = datetime.datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = t.strftime('%Y%m%d')
    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = date_stamp + '/' + region + '/' + serviceName + '/' + 'aws4_request'
    signed_headers = 'content-type;host;x-amz-date;x-amz-target'
    # signing_key = getSignatureKey(secretAccessKey, date_stamp, region, serviceName)
    # signature = hmac.new(signing_key, (signed_headers).encode('utf-8'),hashlib.sha256).hexdigest()
    # authorization_header = algorithm + ' ' + 'Credential=' + accessKey + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    bulkLookup('contacts.csv')
    # lookUp('+16462280241')