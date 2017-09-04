import urllib.request, base64
from datetime import datetime
import xml.etree.cElementTree as ET
import json
import xmltodict

# import json as ET

def UpdateTaskTW(task_id, task_name, start_date, end_date):
    company = "project36"
    key = base64.b64encode(b'twp_TRKx81UCnv4deufBFU2b85350cXo:xxx')
    task_id = "6183721"

    task_name = task_name
    start_date = start_date
    due_date = end_date

    root = ET.Element("request")
    todo_el = ET.SubElement(root, "todo-item")
    content_el = ET.SubElement(todo_el, "content")
    id_el = ET.SubElement(todo_el, "id")
    start_date_el = ET.SubElement(todo_el, "start-date")
    due_date_el = ET.SubElement(todo_el, "due-date")

    content_el.text = task_name
    start_date_el.text = start_date
    due_date_el.text = due_date
    id_el.text = task_id

    json_string = ET.tostring(root, encoding="utf-8", method="xml")
    print("**********+json-string**************")
    print(json_string.decode())

    request = urllib.request.Request(
        "https://{0}.teamwork.com/tasks/{1}.json".format(company, task_id),
        json_string)
    print(request)
    request.add_header("Authorization", "BASIC " + key.decode())
    request.add_header("Content-type", "application/json")
    request.get_method = lambda: "PUT"
    print(request.header_items())
    response = urllib.request.urlopen(request)
    data = response.read()
    print(data)
