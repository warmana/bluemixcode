import os
import json
from time import gmtime, strftime

try:
  from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
  from SocketServer import TCPServer as Server
except ImportError:
  from http.server import SimpleHTTPRequestHandler as Handler
  from http.server import HTTPServer as Server

# Enable the required Python libraries.

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

# This is the name of the database we are working with.
databaseName = "databasedemo"

# Read port selected by the cloud for our application
PORT = int(os.getenv('PORT', 8000))
# Change current directory to avoid exposure of control files
os.chdir('static')

filename = "index.html"

target = open(filename, 'w')

target.truncate()

target.write("<html><head><title>Cloudant Python Demo</title></head><body><p>Log of Cloudant Python steps...</p><pre>")

target.write("====\n")
target.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
target.write("\n====\n\n")


if 'VCAP_SERVICES' in os.environ:
  vcap_servicesData = json.loads(os.environ['VCAP_SERVICES'])
  target.write("Got vcap_servicesData\n")
  cloudantNoSQLDBData = vcap_servicesData['cloudantNoSQLDB']
  target.write("Got cloudantNoSQLDBData\n")
  credentials = cloudantNoSQLDBData[0]
  credentialsData = credentials['credentials']
  target.write("Got credentialsData\n\n")
  serviceUsername = credentialsData['username']
  target.write("Got username: ")
  target.write(serviceUsername)
  target.write("\n")
  servicePassword = credentialsData['password']
  target.write("Got password: ")
  target.write(servicePassword)
  target.write("\n")
  serviceURL = credentialsData['url']
  target.write("Got URL: ")
  target.write(serviceURL)
  target.write("\n")
  client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
  client.connect()
  myDatabaseDemo = client.create_database(databaseName)
  if myDatabaseDemo.exists():
    target.write("'{0}' successfully created.\n".format(databaseName))
  target.write("----\n")
  jsonDocument = {
    "rightNow": strftime("%Y-%m-%d %H:%M:%S", gmtime())
  }
  newDocument = myDatabaseDemo.create_document(jsonDocument)
  if newDocument.exists():
    target.write("Document successfully created.\n")
  target.write("----\n")
  client.disconnect()



target.write("\n====\n")
target.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
target.write("\n====\n")

target.write("</pre></body></html>")

target.close()

httpd = Server(("", PORT), Handler)
try:
  print("Start serving at port %i" % PORT)
  httpd.serve_forever()
except KeyboardInterrupt:
  pass
httpd.server_close()

