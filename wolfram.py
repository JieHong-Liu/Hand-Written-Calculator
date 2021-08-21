import requests
import xmltodict
import json
from urllib import parse


def evaluation(question):
    try:
        appid = 'L6A69L-RRJU9794TQ'
        # question = '21=5x%2Bsin(30)'
        # if('+' in question):
        #     question = question.replace('+', '%2B')
        question = parse.quote(question.encode("utf-8"))

        print(question)
        url = 'http://api.wolframalpha.com/v2/query?appid='+appid+'&input=solve+'+question
        r = requests.get(url)

        dictionary = xmltodict.parse(r.text)
        json_object = json.dumps(dictionary)
        json_file = json.loads(json_object)

        # print(json_file['queryresult']['pod'])
        if(json_file['queryresult']['pod'][0]['@title'] == 'Indefinite integral'):
            return (json_file['queryresult']['pod'][0]['subpod']['plaintext'])
        elif(json_file['queryresult']['pod'][0]['@title'] == 'Definite integral'):
            return (json_file['queryresult']['pod'][0]['subpod']['plaintext'])
        elif(json_file['queryresult']['pod'][0]['@title'] == 'Limit'):
            return (json_file['queryresult']['pod'][0]['subpod']['plaintext'])
        elif(json_file['queryresult']['pod'][0]['@title'] == 'Input interpretation'):
            return (json_file['queryresult']['pod'][1]['subpod'][0]['plaintext'])
        elif (json_file['queryresult']['pod'][0]['@title'] == 'Input'):
            return (json_file['queryresult']['pod'][1]['subpod']['plaintext'])
        else:
            # 'Input interpretation'
            # dircet show answer without calculating
            return (json_file['queryresult']['pod'][1]['subpod']['plaintext'])
    except:
        return question


# print(evaluation('1+2+3'))
