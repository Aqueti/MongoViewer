"""
Tools to assist in communication between the interface and MongoDB
"""

from pymongo import MongoClient
from json import dumps
from bson.son import SON

from pprint import pprint

class MongoInterface():

    # Connect to the local client
    def __init__(self):
        super().__init__()
        myclient = "localhost:27017"
        self.client = MongoClient('mongodb://'+ myclient)

    # Used to change the client 
    def changeclient(self, clientname):
        self.client = MongoClient('mongodb://'+ clientname)
 
    # Name
    def createdb(self,dbname, colname):
        temp = {"temp":"temp"}
        if dbname in self.client.list_database_names():
            pass
        else:
            self.client[dbname][colname].insert_one(temp)
            self.client[dbname][colname].delete_one(temp)

    # Name
    def deletedb(self, dbname):
        deleteme = self.client[dbname].list_collection_names()
        if dbname in self.client.list_database_names():
            for collection in deleteme:
                self.client[dbname][collection].drop()

    # Returns a list of all of the databases
    def getdblist(self):
        return self.client.list_database_names()

    # Name
    def createcol(self, dbname, colname):
        temp = {"temp":"temp"}
        if colname in self.client[dbname].list_collection_names():
            pass
        else:
            self.client[dbname][colname].insert_one(temp)
            self.client[dbname][colname].delete_one(temp)

    # Name
    def deletecol(self, dbname, colname):
        self.client[dbname][colname].drop()

    # Returns a list of all of the collections
    def getcolllist(self):
        colls = []
        for databse in self.client.list_database_names():
            colls.append(self.client[databse].list_collection_names())
        return colls

    # Gets the schema for the object in the form of a json object

    def getjsonschema(self, dbname,colname):
        pgs = self.client[dbname].command('listCollections')['cursor']['firstBatch']
        target_collection = colname

        for dictionary in pgs:
            if dictionary['name'] == target_collection:
                try:
                    return dumps((dictionary['options']['validator']['$jsonSchema']))
                except KeyError:
                    pass 
                try: 
                    return dumps((dictionary['options']['validator']))
                except KeyError:
                    return "null"

    # Equivelent MongoDB command    
    #db.runCommand({collMod:"nameofcollection", {validator: {schema}}})

    # This command is finnicky. There is a problem with pymongo where sometimes, it doesn't 
    #  realize that 'validator' is a real command that it can run on it's collections. 
    # I assure you that it is.

    # Takes a schema and applies it to a collection 
    def editschema(self, dbname, colname, schema): 
        if dbname not in self.client.list_database_names():
            self.createdb(dbname,colname)
        i = 0
        while i < 10:
            try:
                self.client[dbname].command({'collMod':str(colname),'validator':schema})
                return
            except:
                self.editschema(dbname, colname, schema)
                i += 1
    
    # This function gets the database and uses tostring() to turn any objects or functions
    # that the browser doesn't like into strings
    def getwholedatabase(self, dbname, colname):
        data = self.findmany(dbname,colname,{})
        newdata = self.tostring(data)
        return newdata

    # These functions turns everything that is not an object into strings so that
    # the browser doesn't get some unexpected function like Objectid(...) or datetime.datetime
    # If it detects an object, it recurses inside of the object and turns it's contents into strings
    #  instead of turning the whole object into a string.
    def tostring(self, dblist):
        for document in dblist:
            self.stringdict(document)
        return dblist

    def stringdict(self, dictionary):
        for key in dictionary:
            if isinstance(dictionary[key],dict):
                self.stringdict(dictionary[key])
            else:
                dictionary[key] = str(dictionary[key])


    # These functions all do what their names imply
    def findone(self, dbname, colname, query):
        return self.client[dbname][colname].find_one(query)

    def findmany(self, dbname, colname, query):
        return list(self.client[dbname][colname].find(query))

    def deleteone(self, dbname, colname, query):
        self.client[dbname][colname].delete_one(query)

    def deletemany(self, dbname, colname, query):
        self.client[dbname][colname].delete_many(query)

    def addone(self, dbname, colname, inp):
        self.client[dbname][colname].insert_one(inp)

    def addmany(self, dbname, colname, inp):
        self.client[dbname][colname].insert_many(inp)
    



    # Used to get headers for a possible table view in the future

    def getheaders(self, dbname, colname):
        data = self.findmany(dbname,colname,{})
        headers = []
        for document in data:
            for item in document:
                if item == "_id":
                    fitem = ({"title" : item, "align": "left"})
                else:
                    fitem = ({"title" : item})
                if fitem not in headers:
                    headers.append(fitem)
        return headers

    # These don't work yet
    def editonedoc(self, dbname, colname, query, inp):
        self.client[dbname][colname].update_one(query,inp)

    def editmanydoc(self, dbname, colname, query, inp):
        self.client[dbname][colname].update_many(query,inp)

# testing 

MI = MongoInterface()

dbname = "new"
colname = 'students'
query = {"name":"Company Inc"}
inp = {"newthing":"new"}
test = [{1: 'thing two'}]

schema = {'required': 
        ['name', 'year', 'major', 'gpa'], 
    'properties': 
        {'major': {'enum': ['Math', 'English', 'Computer Science', 'History', None], 'description': 'can only be one of the enum values and is required'}, 
        'gpa': {'minimum': 0.0, 'description': 'must be a double and is required', 'bsonType': ['double']},
        'year': {'exclusiveMaximum': False, 'minimum': 2017.0, 'maximum': 3017.0, 'description': 'must be an integer in [ 2017, 3017 ] and is required', 'bsonType': 'int'}, 
        'name': {'description': 'must be a string and is required', 'bsonType': 'string'},
        'gender': {'description': 'must be a string and is not required', 'bsonType': 'string'}, 
        'address.street': {'description': 'must be a string and is required', 'bsonType': 'string'}, 
        'address.city': {'description': 'must be a string and is required', 'bsonType': 'string'}}, 
    'bsonType': 
        'object'
    }

