import base64
from  urllib.request import *

company = "YOUR_TEAMWORK_SITE_NAME"
key = "YOUR_API_KEY"
action = "projects.json"

request = Request("https://{0}.teamwork.com/{1}".format(company, action))
request.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))

response = urlopen(request)
data = response.read()

print (data)
