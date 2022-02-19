import requests
import json

url = "https://pinpoint.us-east-1.amazonaws.com/v1/phone/number/validate"

payload = json.dumps({
  "PhoneNumber": "+13213451680"
})
headers = {
  'Content-Type': 'application/json',
  'X-Amz-Content-Sha256': 'beaead3198f7da1e70d03ab969765e0821b24fc913697e929e726aeaebf0eba3',
  'X-Amz-Date': '20211113T125326Z',
  'Authorization': 'AWS4-HMAC-SHA256 Credential=AKIATD3A3J6MK6ZIWRN6/20211113/us-east-1/mobiletargeting/aws4_request, SignedHeaders=content-type;host;x-amz-content-sha256;x-amz-date, Signature=680db03997c83d5954d4d83a2a80427fc65ca88aef7ee52d64125e5d72c2ccde'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
