import json
import urllib.request, base64
from datetime import datetime
import xml.etree.cElementTree as ET
import ast

def add_project(name_project, description_project, start_date, end_date):
    company = "project36"
    key = base64.b64encode(b'twp_TRKx81UCnv4deufBFU2b85350cXo:xxx')
    project_name = name_project
    project_description =  description_project
    start_date = start_date
    due_date = end_date

    root = ET.Element("request")
    todo_el = ET.SubElement(root, "project")
    content_el = ET.SubElement(todo_el, "name")
    description_el = ET.SubElement(todo_el, "description")
    start_date_el = ET.SubElement(todo_el, "startDate")
    due_date_el = ET.SubElement(todo_el, "endDate")

    content_el.text = project_name
    description_el.text = project_description
    start_date_el.text = start_date
    due_date_el.text = due_date

    action = "projects.json"

    json_string = ET.tostring(root, encoding="utf-8", method="xml")

    print(json_string)

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

def UpdateProjectTW(project_id, project_name, start_date, end_date, description ):
    company = "project36"
    key = base64.b64encode(b'twp_TRKx81UCnv4deufBFU2b85350cXo:xxx')
    projectt_id = project_id
    print(project_id)
    project_name = project_name
    project_description = description
    start_date = start_date
    due_date = end_date

    root = ET.Element("request")
    todo_el = ET.SubElement(root, "project")
    content_el = ET.SubElement(todo_el, "name")
    description_el = ET.SubElement(todo_el, "description")
    start_date_el = ET.SubElement(todo_el, "startDate")
    end_date_el = ET.SubElement(todo_el, "endDate")

    content_el.text = project_name
    description_el.text = project_description
    start_date_el.text = start_date
    end_date_el.text = due_date

    json_string = ET.tostring(root, encoding="utf-8", method="xml")
    print("**********+json-string**************")
    print(json_string.decode())

    request = urllib.request.Request(
        "https://{0}.teamwork.com/projects/{1}.json".format(company, projectt_id),
        json_string)
    print(request)
    request.add_header("Authorization", "BASIC " + key.decode())
    request.add_header("Content-type", "application/json")
    request.get_method = lambda: "PUT"
    print(request.header_items())
    response = urllib.request.urlopen(request)

    data = response.read()
    print(request.get_method())
    print(data)

def DeleteProjectTW(project_id):
    company = "project36"
    key = base64.b64encode(b'twp_TRKx81UCnv4deufBFU2b85350cXo:xxx')
    project_id = project_id
    request = urllib.request.Request(
        "https://{0}.teamwork.com/projects/{1}.json".format(company, project_id))
    print(request)
    request.add_header("Authorization", "BASIC " + key.decode())
    request.add_header("Content-type", "application/json")
    request.get_method = lambda: "DELETE"
    print(request.header_items())
    response = urllib.request.urlopen(request)

    data = response.read()
    print(request.get_method())
    print(data)
