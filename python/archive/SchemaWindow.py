#!/usr/bin/python3
# SchemaEditor.py

from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QVBoxLayout, QHBoxLayout, QLabel
from SmartWidget import SmartWidget
import json
import sys


"""
def SchemaWindow
       #Determine screen setting
       geo         = self.frameGeometry()
       self.width  = QDesktopWidget().availableGeometry().width();
       self.height = QDesktopWidget().availableGeometry().height();

       #Define window par meters
       self.resize(self.width*.5, self.height*.5 )
       self.setWindowTitle("SmartWidget unit test")
       self.show()

       self.mainLayout = QVBoxLayout()
#       self.setLayout( self.mainLayout )

       #Create title
       self.titleLayout = QHBoxLayout()
       self.titleLayout.addStretch(1)
       title = QLabel()
       title.setText("SmartWidget Unit Test")
       self.titleLayout.addWidget(title)
       self.titleLayout.addStretch(1)
       self.mainLayout.addLayout( self.titleLayout )

        """
##
# \brief This class generates a schema editor window
class SchemaView( ):
    def updateSchemaInfo(self):
        value = """
{
    "array": {
        "bsonType": "object",
        "description": "array object",
        "properties": {
            "bsonType": {
                "description": "base type for the variable",
                "enum": [
                    "array"
                ]
            },
            "description": {
                "bsonType": "string",
                "description": "provides a description of the value"
            },
            "items": {
                "bsonType": "object",
                "description": "Defines the schema for array items",
                "properties": {
                    "bsonType": {
                        "description": "base type for the variable",
                        "enum": [
                            "string"
                        ]
                    }
                },
                "required": [
                    "bsonType"
                ]
            },
            "maxItems": {
                "bsonType": "int",
                "description": "maximum number of elements"
            },
            "minItems": {
                "bsonType": "int",
                "description": "minimum number of elements"
            }
        }
    },
    "bool": {
        "bsonType": "object",
        "description": "boolean value",
        "properties": {
            "bsonType": {
                "description": "base type for the variable",
                "enum": [
                    "bool"
                ]
            },
            "description": {
                "bsonType": "string",
                "description": "provides a description of the value"
            }
        }
    },
    "double": {
        "bsonType": "object",
        "description": "double value",
        "properties": {
            "bsonType": {
                "description": "base type for the variable",
                "enum": [
                    "double"
                ]
            },
            "description": {
                "bsonType": "string",
                "description": "provides a description of the value"
            },
            "maximum": {
                "bsonType": "double",
                "description": "maximum value for the double"
            },
            "minimum": {
                "bsonType": "double",
                "description": "minimum value for the double"
            }
        }
    },
    "int": {
        "bsonType": "object",
        "description": "integer values",
        "properties": {
            "bsonType": {
                "description": "base type for the variable",
                "enum": [
                    "int"
                ]
            },
            "description": {
                "bsonType": "string",
                "description": "provides a description of the value"
            },
            "maximum": {
                "bsonType": "int",
                "description": "maximum value for the integer"
            },
            "minimum": {
                "bsonType": "int",
                "description": "minimum value for the integer"
            }
        }
    },
    "object": {
        "bsonType": "object",
        "properties": {
            "bsonType": {
                "description": "base type for the variable",
                "enum": ["string","int","double", "bool","array","object"]
            },
            "description": {
                "bsonType":"string",
                "description":"what the object is for"
            }
        }
    },
    "string": {
        "bsonType": "object",
        "description": "An alphanumeric  sequence of characters",
        "properties": {
            "bsonType": {
                "description": "base type for the variable",
                "bsonType":"string"
            },
            "description": {
                "bsonType": "string",
                "description": "provides a description of the value"
            }
        }
    }
} """
        self.schemaInfo  = json.loads( value )
  
    ##
    # \brief Initialization function
    # \param [in] schema initialization schema
    def __init__(self):
        self.updateSchemaInfo()
        self.schema = {}

    ##
    # \brief validate a schema. 
    # \return true on success, false on failure
    def validateSchema( self, schema ):
        #make sure the schema 
        if not isinstance( schema, object):
            print("INVALID Schema: Not an object")
            return False

        return True


    #Initialize function
    # param [in] schema scheme for the windows that is being drawn. Default=None
    # return
    #
    # This function initializes a SchemaView object based on the given schema. The
    # provided schema is essentially the value for the SmartWidget that is created.
    def init(self, schema=None):
        print("Initializing with schema: "+str(schema))
        self.value=schema

        #Generate reference schema. This will be used for all objects
        self.refSchema = self.schemaInfo["object"]
        schema = {}

        #If we already have some properties, add these to our refSchema
        if "properties" in schema.keys():
            #For each key type, generate a new object from schemaInfo
            for k in schema["properties"].keys():

                #Get the bsonType for this object
                bsonType = schema["properties"][k]["bsonType"]

                #Add the new object to the ref schema
                self.refSchema["properties"][k] = self.schemaInfo[bsonType]
             
                """
                for k2 in self.refSchema["properties"].keys():
                    if k2 in schema["properties"]:
                        self.value[k2] = schema["properties"][k2]
                    else:
                        self.value[k2] = None


                print("RefSchema: "+str(self.refSchema))

                """
        else:
            self.value={}
            self.value["root"]=self.schemaInfo["object"]
                
        print()
        print("Value: "+str(self.value))
        print("Ref: "+str(self.refSchema))
        print()



        print("start")
        self.schemaWidget = SmartWidget().init("schema", self.value, self.refSchema, showSchema=True)

        print("finish")
        

        return self



class SchemaWindow( QWidget ):
    def __init__(self, schema={}):
        self.schema = schema

      
        ###############
        # Create viewing application
        ###############
        super().__init__()

        #Determine screen settings
        geo         = self.frameGeometry()
        self.width  = QDesktopWidget().availableGeometry().width();
        self.height = QDesktopWidget().availableGeometry().height();

        #Define window par meters
        self.resize(self.width*.5, self.height*.5 )
        self.setWindowTitle("Schema Editor Window")


        self.mainLayout = QVBoxLayout()
#        self.setLayout( self.mainLayout )

        #Create title
        self.titleLayout = QHBoxLayout()
        self.titleLayout.addStretch(1)
        title = QLabel()
        title.setText("SmartWidget Unit Test")
        self.titleLayout.addWidget(title)
        self.titleLayout.addStretch(1)
        self.mainLayout.addLayout( self.titleLayout )

        self.schemaView = SchemaView().init(self.schema)

#        widget = SmartWidget().init("test",{},{"bsonType":"string"})
#        self.mainLayout.addWidget( widget.frame )

        self.mainLayout.addWidget( self.schemaView.schemaWidget.frame )

        self.setLayout(self.mainLayout)

        self.show()

if __name__ == '__main__':
    app = QApplication( sys.argv )


#    testSchema = {'bsonType': 'object', 'description': 'object schema', 'properties': {'name':{"bsonType":"string"}}}
#    testSchema = {'bsonType': 'object'}
    testSchema = {}
    window = SchemaWindow(testSchema)

    sys.exit(app.exec_())

