"""
Titre           :fileBrowser.py
Description     :Un explorateur de fichier fait avec PyQt.
Author          :Xavier Blanchette-Noël (1558701)
Date De Remise: :15/05/19
Usage           :python fileBrowser.py
"""

import sys
import os
import math
import glob
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class FileBrowser(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(FileBrowser, self).__init__(*args, **kwargs)
        #self.location = os.getcwd()
        self.location = os.path.join(str(Path.home()))
        os.chdir(self.location)
        #self.location = "../michel"
        self.left = 500
        self.top = 300
        self.width = 800
        self.height = 500
        self.initUi()

    def initUi(self):
        self.changeWindowTitle(self.location)
        self.setGeometry(self.left, self.top, self.width, self.height)


        widget = QWidget(self)
        self.setCentralWidget(widget)
        self.boxLayout = QVBoxLayout()
        widget.setLayout(self.boxLayout)

        self.createTableWidget()

        self.show()


    def createTableWidget(self):
        fileObjectArray = os.listdir(self.location) #Get the content of the folder. os.listdir() returns an array of file objects.

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(self.getNumberRows(self.location))
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "File Type", "Size"])
        
        row = 0
        for item in fileObjectArray:
            self.tableWidget.setItem(row,0, QTableWidgetItem(os.path.basename(item)))
            self.tableWidget.setItem(row,1, QTableWidgetItem(self.getFileType(item)))
            self.tableWidget.setItem(row,2, QTableWidgetItem(str(math.ceil(os.path.getsize(item) / 1024)) + " kb"))
            row = row + 1

        self.boxLayout.addWidget(self.tableWidget)

    def changeWindowTitle(self, path):
        self.setWindowTitle("File Browser | " + path)

    def getFileType(self, path):
        fileExtensions = {
            ".exe" : "Application",
            ".docx" : "Microsoft Word Document",
            ".mp3" : "Audio File",
            ".jpeg" : "JPEG File",
            ".png" : "PNG File",
            ".jpg" : "JPG File",
            ".txt" : "Text Document",
            ".zip" : "Zip File",
            ".html" : "HTML File",
            ".py" : "Python File",
            ".dat" : "DAT File",
            ".ini" : "Configuration File"
        }
        placeHolderString = ""
        if Path(path).suffix in fileExtensions:
            return fileExtensions.get(Path(path).suffix, False)
        elif os.path.isdir(path) == True:
            return "File Folder"
        else:
            placeHolderString = os.path.splitext(path)[1] + " File" 

            return placeHolderString

    def getNumberRows(self, path):
        i = 0
        for item in os.listdir(path):
            i = i + 1

        return i

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileBrowser()
    sys.exit(app.exec_())