import os
import json

try:
  from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
  from SocketServer import TCPServer as Server
except ImportError:
  from http.server import SimpleHTTPRequestHandler as Handler
  from http.server import HTTPServer as Server

# Read port selected by the cloud for our application
PORT = int(os.getenv('PORT', 8000))
# Change current directory to avoid exposure of control files
os.chdir('static')

filename = "environ.txt"

target = open(filename, 'w')

target.truncate()

for entry in os.environ:
  target.write(entry)
  target.write("\n")

target.write("====\n")

if 'VCAP_SERVICES' in os.environ:
  target.write(os.environ['VCAP_SERVICES'])
  target.write("\n")
  # Now let's parse the JSON...
  vcap_servicesData = json.loads(os.environ['VCAP_SERVICES'])
  target.write("Got vcap_servicesData\n")
  cloudantNoSQLDBData = vcap_servicesData['cloudantNoSQLDB']
  target.write("Got cloudantNoSQLDBData\n")
  credentialsData = cloudantNoSQLDBData['credentials']
  target.write("Got credentialsData\n")
  username = credentialsData['username']
  target.write("Got username\n")
  target.write(username)
  target.write("\n")
  password = credentialsData['password']
  target.write("Got password\n")
  target.write(password)
  target.write("\n")

target.write("====\n")

target.close()

httpd = Server(("", PORT), Handler)
try:
  print("Start serving at port %i" % PORT)
  httpd.serve_forever()
except KeyboardInterrupt:
  pass
httpd.server_close()

