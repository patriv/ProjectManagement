import json
import urllib.request, base64
from datetime import datetime
import xml.etree.cElementTree as ET
import ast

def add_project(name_project, description_project):
    company = "project36"
    key = base64.b64encode(b'twp_TRKx81UCnv4deufBFU2b85350cXo:xxx')
    project_name = name_project
    project_description =  description_project
    due_date = datetime.now().strftime("%Y%m%d")
    data = {}
    root = ET.Element("request")
    todo_el = ET.SubElement(root, "project")
    content_el = ET.SubElement(todo_el, "name")
    description_el = ET.SubElement(todo_el, "description")
    due_date_el = ET.SubElement(todo_el, "due-date")

    content_el.text = project_name
    description_el.text = project_description
    due_date_el.text = due_date

    action = "projects.json"

    json_string = ET.tostring(root, encoding="utf-8", method="xml")

    request = urllib.request.Request(
        "https://{0}.teamwork.com/{1}".format(company, action),
        json_string)
    print(request)
    request.add_header("Authorization", "BASIC " + key.decode())
    request.add_header("Content-type", "application/xml")
    print(request.header_items())
    response = urllib.request.urlopen(request)
    data = response.read()
    #Convierte la data en un diccionario
    x = ast.literal_eval(data.decode())

    return x['id']