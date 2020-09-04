#!/usr/bin/python3

import argparse
from string import Template
import sys
from SmartWidget import SmartWidget
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QMessageBox, QApplication, QVBoxLayout, QHBoxLayout, QDesktopWidget, QLabel, QLineEdit, QFrame
import json
from SmartType import SmartType


#This is the template for all templates...
template = """
{ 
   "bsonType":"dict",
   "template": {
       "key":{"bsonType":"string","required":true},
       "bsonType":{"bsonType":"string", "required":true, "select":%s},
       "required":{"bsonType":"bool","description":"flag to indicate if field is required"},
       "select":{"bsonType":"list", "description":"Must match bsonType"},
       "description":{"bsonType":"string"}
   }
}
""" %json.dumps(SmartType.types)

class TemplateViewer( QWidget ):
    def __init__(self):
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
       self.setWindowTitle("SmartWidget unit test")
       self.show()

       self.mainLayout = QVBoxLayout()
       self.setLayout( self.mainLayout )

       #Create title
       self.titleLayout = QHBoxLayout()
       self.titleLayout.addStretch(1)
       title = QLabel()
       title.setText("Template Editor")
       self.titleLayout.addWidget(title)
       self.titleLayout.addStretch(1)
       self.mainLayout.addLayout( self.titleLayout )

#       template.replace("'",'"')
       print("Default template: "+template)
       tplate = json.loads(str(template))
       print( str(tplate))
       self.dataWidget = SmartWidget()
       self.dataWidget.init("my template", {}, tplate)
       self.mainLayout.addWidget(self.dataWidget.frame)
       self.mainLayout.addStretch(1)

       ###
       # Add a check button
       ###
       self.testButton = QPushButton('Submit',self)
       self.testButton.clicked.connect( lambda: self.submitButtonPressEvent())
       self.mainLayout.addWidget( self.testButton )

      
    def submitButtonPressEvent(self):
       print("Hanlding submit button press")
       print(self.dataWidget.getValue())


def main():
    print("Template Editor")

    app = QApplication( sys.argv)
    window = TemplateViewer()

    #run until we exit
    sys.exit(app.exec_())

if __name__ == '__main__':
    #parse arguments
    main()
