# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 07:56:49 2018

@author: clahn
"""

import sys
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets


class MyStream(QtCore.QObject):
    message = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(MyStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))

    def flush(self):
        sys.stdout = sys.__stdout__
        sys.stdout.flush()

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        #sets minimum size of main window
        self.resize(500, 750)

        #Create lable for enter accession # field
        self.label = QtWidgets.QLabel("Enter Acession #", self)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setMaximumHeight(30)
        #self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        #Creates button to generate DICOM report on click
        self.pushButtonPrint = QtWidgets.QPushButton(self)
        self.pushButtonPrint.setText("Generate DICOM Report")
        self.pushButtonPrint.setFixedSize(QtCore.QSize(160, 25))
        self.pushButtonPrint.clicked.connect(self.on_pushButtonPrint_clicked)

        #textbox to enter accession number as sys.argv1
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.setFixedSize(QtCore.QSize(160, 25))

        #textbox for report
        self.textEdit = QtWidgets.QTextEdit(self)

        #A clear button to remove current report from textEdit and textbox to run new report.
        self.clearButton = QtWidgets.QPushButton(self)
        self.clearButton.setText("Clear Report")
        self.clearButton.setFixedSize(QtCore.QSize(80, 25))
        self.clearButton.clicked.connect(self.textEdit.clear)
        self.clearButton.clicked.connect(self.textbox.clear)

        #add save button and connect to save def
        self.sav_btn = QtWidgets.QPushButton('Save')
        self.sav_btn.setFixedSize(QtCore.QSize(80, 25))
        self.sav_btn.clicked.connect(self.save_text)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutHorizontal = QtWidgets.QHBoxLayout(self) #horizontal
        self.layoutVertical.addWidget(self.label, 0, QtCore.Qt.AlignLeft)
        self.layoutHorizontal.addWidget(self.textbox, 0, QtCore.Qt.AlignLeft)
        
        self.layoutVertical.addLayout(self.layoutHorizontal) #horizontal
        self.layoutHorizontal.addWidget(self.pushButtonPrint, 0, QtCore.Qt.AlignLeft)
        self.layoutHorizontal.addWidget(self.clearButton, 0, QtCore.Qt.AlignRight)
        self.layoutHorizontal.addWidget(self.sav_btn, 0, QtCore.Qt.AlignCenter) #horizontal allignment 
       
        self.layoutVertical.addWidget(self.textEdit)
       


    @QtCore.pyqtSlot()
    def on_pushButtonPrint_clicked(self):
        #I think this is where I want to grab the text entered in self.textbox
        #and set it to a sys.argv1 argument that will be executed in the dicom tools file.
        #variable to capture accession #input
        mytext = self.textbox.text()
        
        '''none of the below subprocess commands will quit the process in Spyder when closing the gui.  
        Better to run program in conda interpreter where this is not a problem. '''
        #cmd = "python H:\\Scripts\\untitled1.py" #this works
        #cmd = "python H:\\Scripts\\dicom_image_report.py" #this does not work
        #cmd = "python W:\\Software\\python\\scripts\\clahn\\untitled1.py" #this does not generate anything       
        #cmd = ["python", "H:\\Scripts\\dicom_image_report2.py"] #works. nothing happens on button push. This points to file without sys.argv argument.
        #cmd = ["python", "H:\\Scripts\\untitled1.py"] #this works as list calling script with no sys.argv
        cmd = ["python", "H:\\Scripts\\dicom_image_report.py", mytext] #Works
        #cmd = ["python", "H:\\Scripts\\untitled0.py", mytext] #This works with sys.argv
        #cmd = ["python", "W:\\Software\\python\\scripts\\clahn\\dicom_image_report.py"] #doesn't work calling physics drive script no sys.argv
        #cmd = ["python", "W:\\Software\\python\\scripts\\clahn\\untitled1.py", mytext] #doesn't work calling physics drive script with sys.argv
        # execute script
        output = subprocess.check_output(cmd)
        #print(subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip())
        print(output.decode('utf-8'))
        #print (output)
 

    @QtCore.pyqtSlot(str)
    def on_myStream_message(self, message):
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.textEdit.insertPlainText(message)

    #function gets text and allows user to save file as .txt to system location of choice.
    def save_text(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', QtCore.QDir.homePath())
        
        if filename[0] != "":
            with open(filename[0], 'w') as f:
                my_text = self.textEdit.toPlainText()
                f.write(my_text)

       
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Image Quality DICOM Report')

    main = MyWindow()
    main.show()

    myStream = MyStream()
    myStream.message.connect(main.on_myStream_message)
    
    sys.stdout = myStream
    sys.exit(app.exec_())
