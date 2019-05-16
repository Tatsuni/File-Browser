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
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path
from fileBrowserFile import *
from fileModel import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QHeaderView
from PyQt5.QtCore import *
from PyQt5 import QtGui

class FileBrowser(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(FileBrowser, self).__init__(*args, **kwargs)
        self.location = str(Path.home())
        self.history = []
        self.historyIndex = 0
        self.initializeHistory()
        self.left = 500
        self.top = 300
        self.width = 800
        self.height = 500


        self.initUi()

    def initUi(self):
        """
        Initializes all the UI components before populating the TableView.
        """
        self.changeWindowTitle()
        self.setWindowIcon(QtGui.QIcon("./fileIcons/icons/folder-network-horizontal-open.png"))
        self.setGeometry(self.left, self.top, self.width, self.height)
        


        #Table View
        self.tableView = QTableView(self)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.doubleClicked.connect(self.handleFileDoubleClick)
        self.setCentralWidget(self.tableView)

        #Back Button
        self.buttonBack = QPushButton()
        self.buttonBack.setIcon(QIcon(QPixmap("./fileIcons/icons/arrow-180.png")))
        self.buttonBack.clicked.connect(self.handleBackButtonClick)
        self.buttonForward = QPushButton()
        self.buttonForward.setIcon(QIcon(QPixmap("./fileIcons/icons/arrow.png")))
        self.buttonForward.clicked.connect(self.handleForwardButtonClick)

        #Delete Button
        self.buttonDelete = QPushButton()
        self.buttonDelete.setIcon(QIcon(QPixmap("./fileIcons/icons/bin-metal-full.png")))
        self.buttonDelete.clicked.connect(self.handleDeleteFile)

        #Rename Button
        self.buttonRename = QPushButton()
        self.buttonRename.setText("Rename Selected File")
        self.buttonRename.clicked.connect(self.handleRenameFile)

        #Copy Button
        self.buttonCopy = QPushButton()
        self.buttonCopy.setText("Copy Selected File")
        self.buttonCopy.clicked.connect(self.handleCopyFile)

        #Paste Button
        self.buttonPaste = QPushButton()
        self.buttonPaste.setText("Paste File")
        self.buttonPaste.clicked.connect(self.handlePasteFile)

        #Cut Button
        self.buttonCut = QPushButton()
        self.buttonCut.setText("Cut File")
        self.buttonCut.setIcon(QIcon(QPixmap("./fileIcons/icons/scissors.png")))
        self.buttonCut.clicked.connect(self.handleCutFile)

        #Initialize horizontal box and add stretch to push buttons at bottom of window.
        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.addStretch(1)
        self.hboxLayout.addWidget(self.buttonBack)
        self.hboxLayout.addWidget(self.buttonForward)
        self.hboxLayout.addWidget(self.buttonDelete)
        self.hboxLayout.addWidget(self.buttonRename)
        self.hboxLayout.addWidget(self.buttonCopy)
        self.hboxLayout.addWidget(self.buttonPaste)
        self.hboxLayout.addWidget(self.buttonCut)

        #Initialize vertical box and add stretch to push buttons at right side of window.
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.addStretch(1)
        self.vboxLayout.addLayout(self.hboxLayout)

        #Add vboxLayout to final boxLayout.
        self.tableView.setLayout(self.vboxLayout)

        self.populateTableView()

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.show()

    def populateTableView(self):
        self.filePaths = os.listdir(self.location)
        self.currentFiles = list(map(lambda filePath: FileBrowserFile(os.path.join(self.location, filePath)), self.filePaths))
        viewModel = FileModel((self.currentFiles))

        self.tableView.setModel(viewModel)
        self.changeWindowTitle()
        if self.historyIndex > 0:
            self.buttonBack.setEnabled(True)
        if self.historyIndex < len(self.history) - 1:
            self.buttonForward.setEnabled(True)

    def changeWindowTitle(self):
        self.setWindowTitle("File Browser | " + self.location)

    def initializeHistory(self):
        """
        Initializes the self.history array and the self.historyIndex based on where the program starts.
        """
        levels = self.location.split("\\")
        for i in range(0, len(levels)):
            if len(self.history) == 0:
                self.history.append(levels[0] + "\\")
            else:
                self.history.append("\\".join(levels[0:i + 1]))

        self.historyIndex = len(self.history) - 1
    
    def errorWindow(self, selector):
        message = QMessageBox()
        message.setGeometry(self.left + self.width // 2 - 100, self.top + self.height // 2 - 50, 1, 1)
        message.setWindowTitle("Attention!")
        if selector == 1:
            message.setText("No file is selected.")            
        elif selector == 2:
            message.setText("No file is copied.")
        elif selector == 3:
            message.setText("Permission denied.")

        message.setStandardButtons(QMessageBox.Ok)

        message.exec_()


    def handleCutFile(self):
        try:
            selected = self.tableView.selectedIndexes()[0].row()
            self.isCutting = True
            self.savedFilePath = self.currentFiles[selected].Path
            # os.rename(self.savedFilePathPath, self.location + "\\" + os.path.basename(self.savedFilePathPath))

            # self.populateTableView()
        except AttributeError:
            self.errorWindow(2)
            
    def handleCopyFile(self):
        try:
            selected = self.tableView.selectedIndexes()[0].row()
            self.savedFilePath = self.currentFiles[selected].Path
        except IndexError:
            self.errorWindow(1)

    def handlePasteFile(self):
        try:
            if os.path.isdir(self.savedFilePath):
                shutil.copytree(self.savedFilePath, self.location + "\\" + os.path.basename(self.savedFilePath))
                if self.isCutting:
                    os.rmdir(self.savedFilePath)
            else:
                shutil.copy2(self.savedFilePath, self.location)
                if self.isCutting:
                    os.remove(self.savedFilePath)

            if self.isCutting: self.isCutting = not self.isCutting

            self.populateTableView()
        except AttributeError:
            self.errorWindow(2)

    def handleRenameFile(self):
        try:
            selected = self.tableView.selectedIndexes()[0].row()
            userInput, ok = QInputDialog.getText(self, 'Rename File', 'Enter the new name:')

            os.rename(self.currentFiles[selected].Path, userInput)

            self.populateTableView()
        except IndexError:
            self.errorWindow(1)

    def handleDeleteFile(self):
        try:
            selected = self.tableView.selectedIndexes()[0].row()
            if os.path.isdir(self.currentFiles[selected].Path) == True:
                shutil.rmtree(self.currentFiles[selected].Path, ignore_errors=True)
            else:
                os.remove(self.currentFiles[selected].Path)

            self.populateTableView()
        except IndexError:
            self.errorWindow(1)

    def handleFileDoubleClick(self, QModelIndex):
        try:
            if os.path.isdir(self.currentFiles[QModelIndex.row()].Path) == True:
                clicked = self.currentFiles[QModelIndex.row()]
                self.location = clicked.Path
                self.historyIndex += 1
                self.history.append(clicked.Path)
                self.history[self.historyIndex:len(self.history) - 1] = []

                self.populateTableView()
            else:
                os.startfile(self.currentFiles[QModelIndex.row()].Path)
        except PermissionError:
            self.errorWindow(3)

    def handleBackButtonClick(self):
        try:
            if self.historyIndex == 0:
                self.buttonBack.setEnabled(False)
            else:
                self.historyIndex = self.historyIndex - 1
                self.location = self.history[self.historyIndex]
                self.populateTableView()
        except PermissionError:
            self.errorWindow(3)

    def handleForwardButtonClick(self):
        try:
            if self.historyIndex == len(self.history) - 1:
                self.buttonForward.setEnabled(False)
            else:
                self.historyIndex = self.historyIndex + 1
                self.location = self.history[self.historyIndex]
                self.populateTableView()
        except PermissionError:
            self.errorWindow(3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileBrowser()
    sys.exit(app.exec_())