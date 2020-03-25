import pycurl
from io import BytesIO
import json
import pandas as pd

def req(endpoint):
    buffer = BytesIO()
    c = pycurl.Curl()

    c.setopt(c.URL, 'https://rxnav.nlm.nih.gov/REST/' + endpoint)
    c.setopt(c.HTTPHEADER, ['Accept:application/json'])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    return(json.loads(body.decode('UTF-8')))

def apiResource():
    res = req('')
    return res['resourceList']['resource']

def formatDf(json):
    datacols = ['rxcui', 'name', 'synonym', 'tty', 'language', 'suppress', 'umlscui']
    df = pd.DataFrame(columns = datacols)
    for i in range(len(json)):
        if 'conceptProperties' in json[i].keys():
            for item in json[i]['conceptProperties']:
                df = df.append(item, ignore_index=True)
    return(df)
        

def getDrugInfo(query):
    res = None
    if type(query) == str:
        try:
            res = req(f"drugs?name={query}")['drugGroup']['conceptGroup']
        except:
            return('Drug not found..')
    elif type(query) == int:
        res = req(f"rxcui/{query}/allrelated")['allRelatedGroup']['conceptGroup']
  
    json = []
    for item in res:
        ## Restrict the output of only specific term types by adding or removing them from the 'if' statement.
        if (item['tty'] == 'SBD' or item['tty'] == 'SCD' or item['tty'] == 'SCDG'):
            json.append(item)

    return(formatDf(json))
