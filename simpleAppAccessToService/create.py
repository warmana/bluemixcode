# Enable the required Python libraries.

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

# Useful variables
serviceUsername = "353466e8-47eb-45ce-b125-4a4e1b5a4f7e-bluemix"
servicePassword = "49c0c343d225623956157d94b25d574586f26d1211e8e589646b4713d5de4801"
serviceURL = "https://353466e8-47eb-45ce-b125-4a4e1b5a4f7e-bluemix.cloudant.com"

databaseName = "databasedemo"

sampleData = [
    [1, "one", "boiling", 100],
    [2, "two", "hot", 40],
    [3, "three", "warm", 20],
    [4, "four", "cold", 10],
    [5, "five", "freezing", 0]
]

# Use Cloudant to create a Cloudant client using account
# client = Cloudant(username, password, account=account)
# or using url
client = Cloudant(serviceUsername, servicePassword, url=serviceURL)

# Connect to the server
client.connect()

# Perform client tasks...
session = client.session()
print 'Username: {0}'.format(session['userCtx']['name'])
print 'Databases: {0}'.format(client.all_dbs())

# Delete a pre-existing instance of the test database.
try :
    client.delete_database(databaseName)
except CloudantException:
    print "{0} does not exist.".format(databaseName)

# Create a fresh instance of the database.
myDatabaseDemo = client.create_database(databaseName)

# Check that the database now exists.
if myDatabaseDemo.exists():
    print "{0} successfully created.".format(databaseName)

# Create documents using the sample data.
for document in sampleData:
    number = document[0]
    name = document[1]
    description = document[2]
    temperature = document[3]

    jsonDocument = {
        "numberField": number,
        "nameField": name,
        "descriptionField": description,
        "temperatureField": temperature
    }

    # Create a document using the Database API
    newDocument = myDatabaseDemo.create_document(jsonDocument)

    # Check that the document exists in the database
    if newDocument.exists():
        print "Document {0} successfully created.".format(number)

# Simple and minimal retrieval of documents.
result_collection = Result(myDatabaseDemo.all_docs)
print "Retrieved minimal document: {0}".format(result_collection[0])

# Simple and full retrieval of documents.
result_collection = Result(myDatabaseDemo.all_docs, include_docs=True)
print "Retrieved full document: {0}".format(result_collection[0])

print "\n\n\n"

# Define the end point and parameters
end_point = '{0}/{1}'.format(serviceURL, databaseName + "/_all_docs")
params = {'include_docs': 'true'}

# Issue the request
response = client.r_session.get(end_point, params=params)

# Display the response content
print response.json()

# Disconnect from the server
client.disconnect()

exit()