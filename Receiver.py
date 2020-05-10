from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
isFullIntensity = 0
isNullIntensity = 0
fullIntensity = 250.0
nullIntensity = 0.0
intensityThreshold = 0.0
currentIntensity = 0.0
reverseHuffmanCode = {'0001':'a', '001111':'b', '10110':'c', '00000':'d', '011':'e', 
'11010':'f', '001100':'g', '1001':'h', '0100':'i', '110110100':'j', 
'1101100':'k', '00001':'l', '11000':'m', '0101':'n', '0010':'o', 
'001110':'p', '110110110':'q', '1010':'r', '1000':'s', '111':'t', 
'10111':'u', '110111':'v', '11001':'w', '110110101':'x', '001101':'y', '110110111':'z'}

def DarkTheme():                                                          #Dark Theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    appctxt.setPalette(palette)

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        self.useStylePaletteCheckBox = QCheckBox("Dark Mode")
        self.useStylePaletteCheckBox.setChecked(False)

        self.createLeftGroupBox()
        self.createRightGroupBox()
        self.createBottomGroupBox()

        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)

        topLayout3 = QHBoxLayout()
        enableOperationMode = QRadioButton("Operation Mode")
        enableSetupMode = QRadioButton("Setup Mode")
        enableOperationMode.setFont(QFont("Times", 9, QFont.Bold))
        enableOperationMode.toggled.connect(self.LeftGroupBox.setEnabled)
        enableOperationMode.toggled.connect(self.RightGroupBox.setDisabled)
        enableSetupMode.setFont(QFont("Times", 9, QFont.Bold))
        enableSetupMode.toggled.connect(self.LeftGroupBox.setDisabled)
        enableSetupMode.toggled.connect(self.RightGroupBox.setEnabled)
        enableOperationMode.setChecked(False)
        enableSetupMode.setChecked(True)
        topLayout3.addWidget(enableOperationMode)
        topLayout3.addWidget(enableSetupMode)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout3, 1, 0, 1, 2)
        mainLayout.addWidget(self.LeftGroupBox, 2, 0, 1, 1)
        mainLayout.addWidget(self.RightGroupBox, 2, 1, 1, 2)
        mainLayout.addWidget(self.bottomGroupBox, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Quantum Telery")
        self.changeStyle('Fusion')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(self.originalPalette)
        else:
            QApplication.setPalette(QApplication.style().standardPalette())

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createLeftGroupBox(self):
        self.LeftGroupBox = QGroupBox("Operation Mode")

        modelabel = QLabel('Transmision Modes')
        modelabel.setFont(QFont("Times", 8, QFont.Bold))
        
        radioButton1 = QRadioButton("Bit Mode")
        radioButton2 = QRadioButton("Word Mode")
        radioButton1.setChecked(True)

        modelabel2 = QLabel('Modulation Schemes')
        modelabel2.setFont(QFont("Times", 8, QFont.Bold))
        
        radioButton3 = QRadioButton("Unibit Mode")
        radioButton4 = QRadioButton("Dibit Mode")
        radioButton3.setChecked(True)

        layout1 = QVBoxLayout()
        layout1.addWidget(modelabel)
        layout1.addWidget(radioButton1)
        layout1.addWidget(radioButton2)
        layout1.addStretch(1)
        
        layout2 = QVBoxLayout()
        layout2.addWidget(modelabel2)
        layout2.addWidget(radioButton3)
        layout2.addWidget(radioButton4)
        layout2.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addStretch(1)
        self.LeftGroupBox.setLayout(layout)

    def createRightGroupBox(self):
        self.RightGroupBox = QGroupBox("Setup Mode")
        #enableOperationModeCheckBoxR = QCheckBox("Enable Operation Mode")
        #enableOperationModeCheckBoxR.setFont(QFont("Times", 9, QFont.Bold))
        
        fullIntensity = QPushButton("Fix Full Intensity")
        fullIntensity.clicked.connect(fixFullIntensity)

        nullIntensity = QPushButton("Fix Null Intensity")
        nullIntensity.clicked.connect(fixNullIntensity)

        heightLabel = QLabel()

        self.intensityReceived = QLineEdit()
        intensityReceivedLabel = QLabel("Intensity Received: ")
        intensityReceivedLabel.setBuddy(self.intensityReceived)

        outputInstanceButton = QPushButton("Find Output Instance")
        outputInstanceButton.clicked.connect(self.findCurrentIntensity)

        layout = QVBoxLayout()
        layout.addWidget(fullIntensity)
        layout.addWidget(nullIntensity)
        layout.addWidget(heightLabel)
        layout.addWidget(heightLabel)
        layout.addWidget(intensityReceivedLabel)
        layout.addWidget(self.intensityReceived)
        layout.addWidget(outputInstanceButton)
        layout.addStretch(1)
        self.RightGroupBox.setLayout(layout)

    def createBottomGroupBox(self):
        self.bottomGroupBox = QGroupBox()

        detectedLine = QLineEdit()
        detectedLineLabel = QLabel("Detected Word/Sequence: ")
        detectedLineLabel.setBuddy(detectedLine)

        layout = QGridLayout()
        layout.addWidget(detectedLineLabel)
        layout.addWidget(detectedLine)

        self.bottomGroupBox.setLayout(layout)

    def findCurrentIntensity(self):
        global currentIntensity
        "get current intensity from device"
        self.intensityReceived.setText(str(currentIntensity))


def fixFullIntensity():
    global isFullIntensity
    global fullIntensity

    if (isFullIntensity==0):
        isFullIntensity = 1
        print("Set Full Intensity", fullIntensity)
        """Insert your code here for fixing Full intensityeg"""

        
        fullIntensity = 250.0 #input from receiver
        setIntensityThreshold()

def fixNullIntensity():
    global isNullIntensity
    global nullIntensity

    if (isNullIntensity==0):
        isNullIntensity = 1
        print("Set Null Intensity", nullIntensity)
        """Insert your code here for Turning Off Light Source"""



        nullIntensity = 0.0 #input from receiver
        setIntensityThreshold()

def setIntensityThreshold():
    global intensityThreshold
    global fullIntensity
    global nullIntensity

    if(isFullIntensity==1 and isNullIntensity==1):
        intensityThreshold = (fullIntensity + nullIntensity)/2
        print("Intensity Threshold Set", intensityThreshold)

def huffmanDecoding():
    global reverseHuffmanCode
    receivedCode = '010110000001000010010'
    index = 0
    count = len(receivedCode)
    msg = receivedCode[index]
    output = ''
    while(count):
        if(reverseHuffmanCode.get(msg)==None):
            index+=1
            msg = msg + receivedCode[index]
        else:
            output = output + reverseHuffmanCode.get(msg)
            index+=1
            if(index<len(receivedCode)):
                msg = receivedCode[index]
        count-=1
    print(output)


if __name__ == '__main__':
    appctxt = QApplication([])       # 1. Instantiate ApplicationContext
    #window.setWindowIcon(QIcon('Icon.ico'))
    gallery = WidgetGallery()
    gallery.show()
    exit_code = appctxt.exec_()      # 2. Invoke appctxt.exec_()
    sys.exit(exit_code)
