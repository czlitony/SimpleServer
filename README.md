# SimpleServer
Using python simpleHttpServer to transmit file.

Both server and client python scripts works well on python2.7 .
## server
Run the command:
```
python SimpleServer.py
```
The server will listen at port 8000, you can open your web browser and visit <http://localhost:8000>.
When the server receives the file, it will save the file at the same folder with the file SimpleServer.py .
## client
Library 'requests' is needed here, [click](http://docs.python-requests.org/en/master/user/install/#install) to get it.  
To send a file, you can modify the file sender.py, then run the command:
```
python sender.py
```

You can modify the file depending on your requirements.



