
import json
import requests
import sys

def get_rest_url(model_name, host='127.0.0.1', port='8501', verb='predict', version=None):
    """ generate the URL path"""
    url = "http://{host}:{port}/v1/models/{model_name}".format(host=host, port=port, model_name=model_name)
    if version:
        url += 'versions/{version}'.format(version=version)
    url += ':{verb}'.format(verb=verb)
    return url

def get_model_prediction(model_input, model_name='amrvw', signature_name='serving_default'):
    """ no error handling at all, just poc"""

    url = get_rest_url(model_name)
    #In the row format, inputs are keyed to instances key in the JSON request.
    #When there is only one named input, specify the value of instances key to be the value of the input:
    
    # in our case, no difference between using "instances" or "inputs".
    # data = {"instances": [model_input]}
    data = {"inputs": [model_input]}
    
    rv = requests.post(url, data=json.dumps(data))
    if rv.status_code != requests.codes.ok:
        rv.raise_for_status()
    
    return rv.json()['predictions']

if __name__ == '__main__':

    print("\nGenerate REST url ...")
    url = get_rest_url(model_name='amrvw')
    print(url)
    
    while True:
        print("\nEnter an Amazon review [:q for Quit]")
        if sys.version_info[0] <= 3:
            sentence = input()
        if sentence == ':q':
            break
        model_input = sentence
        model_prediction = get_model_prediction(model_input)
        print("The model predicted ...")
        print(model_prediction)
