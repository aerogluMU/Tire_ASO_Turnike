import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from turnike import *
from turnikePort import *

app = QApplication(sys.argv)
window = QMainWindow()
window_Tur = QMainWindow()
ui = Ui_TurnikePort()
secUi = Ui_TurnikeDurum()

ui.setupUi(window)
window.show()

# Veritabanı İşlemleri
import sqlite3

conn = sqlite3.connect("customers.db")

islem = conn.cursor()
conn.commit()

# FUNCTIONS

def updateCustomerCount(cardid):
    try:
        islem.execute("update customer set count=? where cardid=?",(0,cardid))
        conn.commit()
    except Exception as error:
        pass
    
# Port Window
import serial.tools.list_ports
import serial

ser = serial.Serial()

def listPorts():
    ports = serial.tools.list_ports.comports()
    ui.comList_Turnike.clear()
    for port, desc, hwis in sorted(ports):
        ui.comList_Turnike.addItem(str(port+" "+desc))
    
def selectPort():
    global ser
    ser.close()
    portStr = ui.comList_Turnike.selectedItems()
    portStr = portStr[0].text()
    port = int(portStr[3:4:1])
    
    try:
        ser = serial.Serial(port='COM%d' % (int(port)), baudrate = 9600,  bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0)
        ui.statusbar.showMessage("Başarılı bir şekilde bağlantı sağlandı.",5000)
        secWindow()
        window.close()
    except Exception as error:
        ui.statusbar.showMessage("Başarısız!!! Bağlantı sağlanamadı." + str(error))

def secWindow():
    secUi.setupUi(window_Tur)
    window_Tur.show()
    global ser
    rxbuf = ""
    while 1:
        res = ser.read().decode("utf-8")
        if(res != '\n'):
            rxbuf += res
        else:
            ui.lne_cardid.setText(rxbuf)
            ui.statusbar.showMessage("Kart başarı ile okundu.",5000)
            break

    
ui.btn_reflesh_turnike.clicked.connect(listPorts)
ui.btn_choose_turnike.clicked.connect(selectPort)

listPorts()

sys.exit(app.exec_())