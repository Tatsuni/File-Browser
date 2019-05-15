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
from fileBrowserFile import *
from fileModel import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class FileBrowser(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(FileBrowser, self).__init__(*args, **kwargs)
        self.location = os.path.join(str(Path.home()))
        os.chdir(self.location)
        self.left = 500
        self.top = 300
        self.width = 800
        self.height = 500
        self.initUi()

    def initUi(self):
        self.changeWindowTitle(self.location)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tableView = QTableView(self)
        self.tableView.setSelectionBehavior(QtWidgets.SelectRows)

        self.setCentralWidget(self.tableView)
        self.boxLayout = QVBoxLayout()
        self.tableView.setLayout(self.boxLayout)

        self.createTableWidget()

        self.show()


    def createTableWidget(self):
        filePaths = os.listdir(self.location)
        viewModel = FileModel(list(map(lambda filePath: FileBrowserFile(filePath), filePaths)))
        self.tableView.setModel(viewModel)

        self.boxLayout.addWidget(self.tableView)

    def changeWindowTitle(self, path):
        self.setWindowTitle("File Browser | " + path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileBrowser()
    sys.exit(app.exec_())