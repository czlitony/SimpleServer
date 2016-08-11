#coding=utf-8
# import urllib.request
import requests

url = 'http://localhost:8000'
path = u'/home/tony/phonehome/phone_home_data.xml'
print path
files = {'file': open(path, 'rb')}
r = requests.post(url, files=files)
print r.url,r.text

