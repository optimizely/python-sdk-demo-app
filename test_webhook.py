from __future__ import print_function

import requests
import json

# Update project_id
project_id = "<project_id>"

data = {"timestamp": 1463602412, "project_id": project_id, "data": {"cdn_url": "https://cdn.optimizely.com/json/{0}.json".format(project_id), "origin_url": "https://optimizely.s3.amazonaws.com/json/{0}.json".format(project_id), "revision": 15}, "event": "project.datafile_updated"}

r = requests.post("http://127.0.0.1:4001/webhook", data=json.dumps(data), headers={'Content-Type': 'application/json'})

print(r.text)
