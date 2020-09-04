from flask import render_template, send_file, jsonify, request
from app import app
from app.mongointerface import MongoInterface
from pymongo import MongoClient

MI = MongoInterface()

# Home route.
@app.route('/', methods=['GET','POST'])
def index():
   """Main page route."""
   dbs = MI.getdblist()
   colls = MI.getcolllist()
   return render_template('index.html', dbs = dbs, colls = colls, 
   dbnum = len(dbs), colnum = len(colls))

# Collection view route
@app.route('/database/<db>/<coll>', methods=['GET','POST'])
def dbpage(db, coll):
   dbs = MI.getdblist()
   colls = MI.getcolllist()
   title = db + '/' + coll
   dbinfo = MI.getwholedatabase(db,coll)
   route = "Database: \"" + db + "\" Collection: \"" + coll + "\""
   return render_template('database.html', title = title, dbinfo = dbinfo,
   dbs = dbs, colls = colls, route = route, db = db, coll = coll, 
   location = "database", dbnum = len(dbs), colnum = len(colls))

# Schema view route
@app.route('/schema/<db>/<coll>', methods=['GET','POST'])
def schpage(db, coll):
   title = db + '/' + coll
   dbs = MI.getdblist()
   colls = MI.getcolllist()
   route = "Database: \"" + db + "\" Collection: \"" + coll + "\""
   schema = MI.getjsonschema(db,coll)
   return render_template('schema.html', title = title, schema = schema, 
   dbs = dbs, colls = colls, route = route, db = db, coll = coll, location = "schema",
   dbnum = len(dbs), colnum = len(colls))

# This is the route that accepts the schema and hands it off to python to be 
#  applied to the collection
@app.route('/reciever/schema/<db>/<coll>', methods=['POST'])
def recieveSchema(db, coll):
   schema = request.get_json(force=True)
   MI.editschema(db,coll,schema)
   return schema





# These routes are all works in progress 


# Work in progress route for simple queries
@app.route('/database/<db>/<coll>/<field>/<query>', methods=['GET','POST'])
def querypage(db, coll, field, query):
   dbs = MI.getdblist()
   colls = MI.getcolllist()
   title = db + '/' + coll
   fq = {field: query}
   dbinfo = MI.findmany(db,coll, fq)
   route = "Database: \"" + db + "\" Collection: \"" + coll + "\""
   return render_template('database.html', title = title, dbinfo = dbinfo,
   dbs = dbs, colls = colls, route = route, db = db, coll = coll, location = "database",
   dbnum = len(dbs), colnum = len(colls))

# list collections
@app.route('/database/<db>')
def collselect():
   pass

# Route where information is sent to add a document to a collection
@app.route('/<db>/<coll>/add/<item>')
def addpage(db,coll,item):
    pass

# Route where information is sent to delete documents from a collection
@app.route('/<db>/<coll>/delete/<item>')
def delpage(db,coll,item):
    pass
