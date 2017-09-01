import urllib.request, base64
from datetime import datetime
import xml.etree.cElementTree as ET
import json
import xmltodict

# import json as ET

def AddTask(tasklist_id, task_name, start_date, end_date ):
    company = "project36"
    key = base64.b64encode(b'twp_TRKx81UCnv4deufBFU2b85350cXo:xxx')
    tasklist_id = tasklist_id
    task_name = task_name
    start_date = start_date
    due_date = end_date

    root = ET.Element("request")
    todo_el = ET.SubElement(root, "todo-item")
    content_el = ET.SubElement(todo_el, "content")
    start_date_el = ET.SubElement(todo_el, "start-date")
    due_date_el = ET.SubElement(todo_el, "due-date")

    content_el.text = task_name
    start_date_el.text = start_date
    due_date_el.text = due_date

    json_string = ET.tostring(root, encoding="utf-8", method="xml")
    print("**********+json-string**************")
    print(json_string.decode())
    x = json_string.decode()


    z = xmltodict.parse(x)
    print(z)

    r = json.dumps(z)

    print(json.dumps(z))

    request = urllib.request.Request(
        "https://{0}.teamwork.com/todo_lists/{1}/todo_items.json".format(company, tasklist_id),
        json_string)
    print(request)
    request.add_header("Authorization", "BASIC " + key.decode())
    request.add_header("Content-type", "application/json")
    print(request.header_items())
    response = urllib.request.urlopen(request)
    data = response.read()
    print(data)