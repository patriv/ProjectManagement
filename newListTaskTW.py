import ast
import urllib.request, base64
from datetime import datetime
import xml.etree.cElementTree as ET


def NewTaskList(tasklist_name, project_id, project_name):

    company = "project36"
    key = base64.b64encode(b'twp_TRKx81UCnv4deufBFU2b85350cXo:xxx')

    project_id = project_id
    tasklist_name=tasklist_name
    project_name=project_name

    root = ET.Element("request")
    task = ET.SubElement(root,"todo-list")
    name_el = ET.SubElement(task, "name")

    projectName_el=ET.SubElement(task,"projectname")
    content_el = ET.SubElement(task, "projectid")

    name_el.text = tasklist_name
    content_el.text = project_id
    projectName_el.text = project_name

    json_string = ET.tostring(root, encoding="utf-8", method="xml")
    print(json_string)

    request = urllib.request.Request(
            "https://{0}.teamwork.com/projects/{1}/tasklists.json".format(company, project_id),
        json_string)
    print("request**")
    print(request)

    request.add_header("Authorization", "BASIC " +   key.decode())
    request.add_header("Content-type", "application/json")
    print(request.header_items())
    response = urllib.request.urlopen(request)
    data = response.read()
    print (data)
    x = ast.literal_eval(data.decode())

    return x['TASKLISTID']