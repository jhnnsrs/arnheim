import requests

BASEURL = 'http://localhost/api'
CREATOR = 1
VARIETY = 0

def _url(path):
    return BASEURL + path

def add_model(path, json):
    return requests.post(_url('/' + path + '/'), json=json)


print("HALLO")

models = {
    "nodes" : [
        {
            "entityid": 1,
            "name": "MaxISP",
            "nodeclass": "classic-node",
            "path": "MaxIssSP",
            "channel": "maxisp",
            "inputmodel": '["REPRESENTATION","SLICE"]',
            "outputmodel": '["REPRESENTATION"]',
            "defaultsettings": '{"scale":"5","overwrite":true,"channels":0, "lower": 0, "upper":-1}',
            "creator": CREATOR,
            "variety": VARIETY
        }
    ]
}

for key in models:
    for el in models[key]:
        print(el)
        add_model(key,el)



