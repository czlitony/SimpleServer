#coding=utf-8
import requests

url = 'http://localhost:8000'
path = u'./phone_home_data.xml'
print path
files = {'file': open(path, 'rb')}
r = requests.post(url, files=files)
print r.url,r.text

