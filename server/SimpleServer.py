#!/usr/bin/python
# -*- coding: utf-8 -*-

import SimpleHTTPServer
import SocketServer
import logging
import cgi
import os

from xml.etree import ElementTree as ET 

import collections
import json

# from xml.dom.minidom import parse
# import xml.dom.minidom 

PORT = 8000

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.info(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # logging.info(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # A nested FieldStorage instance holds the file
        fileitem = form['file']
        # Test if the file was uploaded
        if fileitem.filename:
            # strip leading path from file name to avoid directory traversal attacks
            fn = os.path.basename(fileitem.filename)
            # open('files/' + fn, 'wb').write(fileitem.file.read())
            open(fn, 'wb').write(fileitem.file.read())
            print 'The file "' + fn + '" was received successfully'
            
            # check if the received xml file is well-formed
            try:  
                ET.parse(fileitem.filename)  
                print 'The file "'+ fn +'" is a well-formed XML file'  
            except Exception,e:  
                print 'The file "'+ fn +'" is not a well-formed XML file'  
                print 'The reason may be：',e

            # parse the xml file into a json file
            data = {}
            data = collections.OrderedDict(data)
            tree = ET.ElementTree(file=fileitem.filename)
            root = tree.getroot()
            config = root.find('config')
            if config is None:
                print "config not found, or config has no subelements"
            else:
                for elem in list(config):
                    data[elem.tag] = elem.attrib['value']
            runtime = root.find('runtime')
            if runtime is None:
                print "runtime not found, or runtime has no subelements"
            else:
                for elem in list(runtime):
                    data[elem.tag] = elem.attrib['value']

            # dump parsed data to phone_home_data.json file
            jsonfile = fileitem.filename.split('.')[0]+'.json'
            with open(jsonfile, 'w') as f:
                json.dump(data, f, indent=4)
            print 'The file "'+ fn +'" was parsed successfully into file "'+jsonfile+'"'
        else:
            print 'No file was uploaded'

        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()