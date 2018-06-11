import requests
import json


def analyze_tone(text):
    username = '4f463b56-0409-40a9-9b21-344b258cfc50'
    password = '20pALcNLDZB3'
    watsonUrl = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2018-04-11'
    headers = {"content-type": "text/plain"}
    data = text
    try:
        r = requests.post(watsonUrl, auth=(username, password), headers=headers,
                          data=data)
        return r.text
    except:
        return False




def display_results(data):
    data = json.loads(str(data))
    print(data)




a = analyze_tone("""Congress president Rahul Gandhi on sunday said the government would be able to instil faith among the young only by competing with China in creating jobs, and asserted the issue would be the central theme for India in the coming years""")
print(a)