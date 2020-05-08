from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
"""import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)
pwm=GPIO.PWM(12,1000)"""
lightSourceStatus = 0
huffmanCode = {'a':'0001', 'b':'101001', 'c':'11001', 'd':'00000', 'e':'100', 
'f':'001100', 'g':'001101', 'h':'0101', 'i':'0100', 'j':'110100101', 
'k':'1101000', 'l':'00001', 'm':'10101', 'n':'0110', 'o':'0010', 
'p':'101000', 'q':'1101001000', 'r':'1011', 's':'0111', 't':'111', 
'u':'00111', 'v':'110101', 'w':'11000', 'x':'11010011', 'y':'11011', 'z':'1101001001'}

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
        self.createProgressBar()

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
        mainLayout.addWidget(self.progressBar, 4, 0, 1, 2)
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
        
        self.radioButton1 = QRadioButton("Bit Mode")
        self.radioButton2 = QRadioButton("Word Mode")
        self.radioButton1.setChecked(True)

        modelabel2 = QLabel('Modulation Schemes')
        modelabel2.setFont(QFont("Times", 8, QFont.Bold))
        
        self.radioButton3 = QRadioButton("Unibit Mode")
        self.radioButton4 = QRadioButton("Dibit Mode")
        self.radioButton3.setChecked(True)

        transmitlabel = QLabel('Word/Bit Sequence')

        self.wordline = QLineEdit()

        layout1 = QVBoxLayout()
        layout1.addWidget(modelabel)
        layout1.addWidget(self.radioButton1)
        layout1.addWidget(self.radioButton2)
        layout1.addStretch(1)
        
        layout2 = QVBoxLayout()
        layout2.addWidget(modelabel2)
        layout2.addWidget(self.radioButton3)
        layout2.addWidget(self.radioButton4)
        layout2.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addWidget(transmitlabel)
        layout.addWidget(self.wordline)
        layout.addStretch(1)
        self.LeftGroupBox.setLayout(layout)

    def createRightGroupBox(self):
        self.RightGroupBox = QGroupBox("Setup Mode")
        #enableOperationModeCheckBoxR = QCheckBox("Enable Operation Mode")
        #enableOperationModeCheckBoxR.setFont(QFont("Times", 9, QFont.Bold))
        
        togglePushButton = QPushButton("Turn On Light Source")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(False)
        togglePushButton.clicked.connect(turnOnLightSource)

        slidertext = QLabel('Intensity')

        self.slider = QSlider(Qt.Horizontal, self.RightGroupBox)
        self.slider.setValue(50)
        self.slider.sliderReleased.connect(self.valuechange)

        heightLabel = QLabel()

        bitComboBox = QComboBox()
        bitComboBox.addItems(["0", "1"])

        bitLabel = QLabel("Select Bit to Transmit: ")
        bitLabel.setBuddy(bitComboBox)

        turnButton = QPushButton("Send Bit")

        layout = QVBoxLayout()
        layout.addWidget(togglePushButton)
        layout.addWidget(heightLabel)
        layout.addWidget(slidertext)
        layout.addWidget(self.slider)
        layout.addWidget(heightLabel)
        layout.addWidget(bitLabel)
        layout.addWidget(bitComboBox)
        layout.addWidget(turnButton)
        layout.addStretch(1)
        self.RightGroupBox.setLayout(layout)

    def createBottomGroupBox(self):
        self.bottomGroupBox = QGroupBox()

        self.bitLabel = QLabel('Character being Transferred: ')
        transmitButton = QPushButton('Transmit')
        transmitButton.clicked.connect(self.transmitMessage)

        layout = QGridLayout()
        layout.addWidget(self.bitLabel)
        layout.addWidget(transmitButton)

        self.bottomGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)

    def valuechange(self):
        print("Slider Value Changed to ")
        print(self.slider.value())
        #pwm.start(self.slider.value())

    def transmitMessage(self):
        errorStatus = 0
        transmissionMessage = str(self.wordline.text())
        if len(transmissionMessage)==0:
            errorStatus = 1
            print("Empty Sequence Error")
            self.bitLabel.setText("Error: Enter Sequence")
        else:
            if self.radioButton1.isChecked():
                transmissionMessage = [i for i in transmissionMessage]
                print("Bit Mode")
                bitFlag = 0
                for i in transmissionMessage:
                    if (i!='0') and (i!='1'):
                        bitFlag += 1
                if bitFlag>0:
                    errorStatus = 1
                    print("Incorrect Binary Sequence Error")
                    self.bitLabel.setText("Error: Enter Correct Binary Sequence")
            else:
                print("Word Mode")
                transmissionMessage = transmissionMessage.split()[0]
                transmissionMessage = [i for i in transmissionMessage]
                temp = []
                for i in transmissionMessage:
                    temp.append(str(bin(ord(i)))[2:])
                transmissionMessage = temp
                    
            if self.radioButton3.isChecked():
                print("UniBit Mode")
            else:
                print("Dibit Mode")
            if(errorStatus==0):
                print(transmissionMessage)
                self.bitLabel.setText("Starting Transmission...")
                huffmanCoding()




def turnOnLightSource():
    global lightSourceStatus
    if (lightSourceStatus==1):
        lightSourceStatus = 0
        print("Light Turned Off")
        #pwm.stop()
    else:
        lightSourceStatus = 1
        print("Light Turned On")
        #pwm.start(50)

def huffmanCoding():
    global huffmanCode
    msg = 'hello'
    msg = [i for i in msg]
    print(msg)
    temp = []
    for i in msg:
        temp.append(huffmanCode.get(i))
    msg = temp
    print(msg)


if __name__ == '__main__':
    appctxt = QApplication([])       # 1. Instantiate ApplicationContext
    #window.setWindowIcon(QIcon('Icon.ico'))
    DarkTheme()
    lightSourceStatus = 0
    gallery = WidgetGallery()
    gallery.show()
    exit_code = appctxt.exec_()      # 2. Invoke appctxt.exec_()
    sys.exit(exit_code)
