import urllib.request, base64
from datetime import datetime
import xml.etree.cElementTree as ET
import json
import xmltodict
#import json as ET

company = "project36"
key = base64.b64encode(b'twp_TRKx81UCnv4deufBFU2b85350cXo:xxx')
# tasklist_id = "642613"
# task_name = "This is an example task."
# due_date = datetime.now().strftime("%Y%m%d")
# data={}
# root = ET.Element("request")
# todo_el = ET.SubElement(root, "todo-item")
# content_el = ET.SubElement(todo_el, "content")
# due_date_el = ET.SubElement(todo_el, "due-date")
#
# content_el.text = task_name
# due_date_el.text = due_date
#
# json_string = ET.tostring(root, encoding="utf-8", method="xml")
# print("**********+json-string**************")
# print(json_string.decode())
# x=json_string.decode()



project_id = "221007"
tasklist_name="prueba json"
project_name="Prueba"
due_date = datetime.now().strftime("%Y%m%d")

#todo_el = ET.SubElement(root, "tasklist")
root = ET.Element("request")
task = ET.SubElement(root,"todo-list")
name_el = ET.SubElement(task, "name")
description_el = ET.SubElement(task, "description")
uncompleted_el = ET.SubElement(task, "uncompleted-count")
projectName_el=ET.SubElement(task,"projectname")
content_el = ET.SubElement(task, "projectid")
#due_date_el = ET.SubElement(todo_el, "due-date")

name_el.text = tasklist_name
content_el.text = project_id
projectName_el.text = project_name
uncompleted_el.text = "2"
#todo_el.text = tasklist_name

#due_date_el.text = due_date

json_string = ET.tostring(root, encoding="utf-8", method="xml")
print(json_string)

request = urllib.request.Request(
        "https://{0}.teamwork.com/projects/{1}/tasklists.json".format(company, project_id),
    json_string)
print("request**")
print(request)

# request = urllib.request.Request(
#         "https://{0}.teamwork.com/todo_lists/{1}/todo_items.xml".format(company, tasklist_id),
#     json_string)
print(request)
request.add_header("Authorization", "BASIC " +   key.decode())
request.add_header("Content-type", "application/json")
print(request.header_items())
response = urllib.request.urlopen(request)
data = response.read()
print (data)