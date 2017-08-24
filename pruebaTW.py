import urllib.request, base64
 
company = "project36"
key = base64.b64encode(b'twp_TRKx81UCnv4deufBFU2b85350cXo:xxx')
print("*******KEYYYYY*********")
print(key)
action = "projects.json"
 
request =  urllib.request.Request("https://{0}.teamwork.com/{1}".format(company, action))


request.add_header("Authorization", "BASIC " + key.decode())
 
response = urllib.request.urlopen(request)
data = response.read()
 
print (data)