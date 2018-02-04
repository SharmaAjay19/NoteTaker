import requests
import json
config = json.load(open('config.json', 'r'))
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': config["LUIS_KEY"],
}

params ={
    # Query parameter
    'q': 'Please note that my name is Ajay',
    # Optional request parameters, set to default values
    'timezoneOffset': '0',
    'verbose': 'false',
    'spellCheck': 'false',
    'staging': 'false',
}

try:
    r = requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/' + config["LUIS_APP_ID"],headers=headers, params=params)
    print(r.json())

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################