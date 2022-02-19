# pip install twilio
# pip install python-dotenv

import os
from os.path import join, dirname
from dotenv import load_dotenv
from twilio.rest import Client
import csv
import time
from shutil import copyfile

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)
ts = str(time.time())

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
    phone_number = client.lookups \
                        .v1 \
                        .phone_numbers(number) \
                        .fetch(type=['carrier'])

    return phone_number.carrier['type']

def bulkLookup(filename):
    copyfile('./input/' + filename, './input/' + filename.split('.')[0] + '-origin' + '.csv')
    allContacts = readCsv('./input/' + filename)
    counter = 1

    for index, contact in enumerate(allContacts[1:len(allContacts)]):
        number = contact[2]

        try:
            type = lookUp(number)
            print('[Type]', type)

            if type == 'mobile':
                writeCsv('./output/' + filename.split('.')[0] + '-' + ts + '.csv', contact)
                overWriteCsv('./input/unexecuted.csv', allContacts[(index + 1):len(allContacts)])

            if counter >= 500:
                time.sleep(5)
                counter = 1

            counter = counter + 1
        except:
            continue

if __name__ == '__main__':
    bulkLookup('contacts.csv')