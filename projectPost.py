import urllib.request, base64
from datetime import datetime
import xml.etree.cElementTree as ET


company = "project36"
key = base64.b64encode(b'twp_TRKx81UCnv4deufBFU2b85350cXo:xxx')

info={"project":{
    "name":"proyecto pruebaaa",
    "description":"Descripcion del proyecto",
    "companyId":"77931",
    "start-date":"",
    "end-date":"",
    "use-tasks" : "1",
    "use-milestones" : "1",
    "use-messages" : "1",
    "use-files" : "1",
    "use-time" : "1",
    "use-notebook" : "1",
    "use-riskregister" : "1",
    "use-links" : "1",
    "use-billing" : "1",
    "start-page": "projectoverview",
    "harvest-timers-enabled": "true",
    "defaultPrivacy": "open"
}}



action = "projects.json"

request = urllib.request.Request("https://{0}.teamwork.com/{1}".format(company, action), info)

# request = urllib.request.Request(
#     "https://{0}.teamwork.com/todo_lists/{1}/todo_items.xml".format(company, tasklist_id),
#     json_string)
print(request)
request.add_header("Authorization", "BASIC " + key.decode())
request.add_header("Content-type", "application/json")
print(request.header_items())
response = urllib.request.urlopen(request)
data = response.read()
print(data)