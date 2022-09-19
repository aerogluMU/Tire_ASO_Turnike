import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from tireaso import *
from tireaso_qt_com_ports import *

app = QApplication(sys.argv)
window = QMainWindow()
window_Com = QMainWindow()
ui = Ui_MainWindow()
secUi = Ui_ComPortWindow()

ui.setupUi(window)
window.show()

# Veritabanı İşlemleri
import sqlite3

conn = sqlite3.connect("customers.db")

islem = conn.cursor()
conn.commit()

table = islem.execute("CREATE TABLE IF NOT EXISTS customer (firstName text,lastName text,cardID text,customerType text,count integer)")
conn.commit()

def addCustomer():
    global ser
    if ser.isOpen():
        first = ui.lne_first.text()
        last = ui.lne_last.text()
        cardid = ui.lne_cardid.text()
        customerType = ui.cb_customerType.currentText()
        if cardid != "":
            try:
                add = "insert into customer (firstName,lastName,cardID,customerType,count) values(?,?,?,?,?)"
                islem.execute(add,(first,last,cardid,customerType,1))
                conn.commit()
                ui.statusbar.showMessage("Müşteri Kaydı Başarılı",10000)
                showCustomers()
            except Exception as error:
                ui.statusbar.showMessage("Başarısız!!! Müşteri Kaydı Eklenemedi." + str(error))
        else:
            ui.statusbar.showMessage("Başarısız!!! CardID boş olamaz. Lütfen kart okutun.")
    else:
        ui.statusbar.showMessage("Başarısız!!! Lütfen üst menüden cihaz seçiniz.")

def showCustomers():
    ui.tableWidget.clear()
    ui.tableWidget.setHorizontalHeaderLabels(("Ad","Soyad","Kart Numarası","Müşteri Tipi","Yemek Hakkı"))
    sorgu = "select * from customer"
    islem.execute(sorgu)
    for indexRow, kayitNumarasi in enumerate(islem):
        for indexCol, kayitCol in enumerate(kayitNumarasi):
            ui.tableWidget.setItem(indexRow,indexCol,QTableWidgetItem(str(kayitCol)))

def cusTypeFilter():
    selectedType = ui.cb_filter.currentText()
    sorgu = "select * from customer where customerType=?"
    islem.execute(sorgu,(selectedType,))
    ui.tableWidget.clear()
    ui.tableWidget.setHorizontalHeaderLabels(("Ad","Soyad","Kart Numarası","Müşteri Tipi","Yemek Hakkı"))
    for indexRow, kayitNumarasi in enumerate(islem):
        for indexCol, kayitCol in enumerate(kayitNumarasi):
            ui.tableWidget.setItem(indexRow,indexCol,QTableWidgetItem(str(kayitCol)))

def removeCustomer():
    remove_msg = QMessageBox.question(window,"Silme Onayı","Seçili müşteriyi silmek istediğinizden emin misiniz?",QMessageBox.Yes | QMessageBox.No)
    
    if remove_msg == QMessageBox.Yes:
        selectedCus = ui.tableWidget.selectedItems()
        removeCus = selectedCus[2].text()
        
        sorgu = "delete from customer where cardID=?"
        try:
            islem.execute(sorgu,(removeCus,))
            conn.commit()
            ui.statusbar.showMessage("Müşteri Kaydı Başarı ile Silindi",10000)
            showCustomers()
        except Exception as error:
            ui.statusbar.showMessage("Başarısız!!! Müşteri Kaydı Silinemedi." + str(error))
    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi.",10000)

def updateCustomer():
    update_msg = QMessageBox.question(window,"Güncelleme Onayı","Seçili müşteriyi güncellemek istediğinizden emin misiniz?",QMessageBox.Yes | QMessageBox.No)
    if update_msg == QMessageBox.Yes:
        try:
            first = ui.lne_first.text()
            last = ui.lne_last.text()
            cardid = ui.lne_cardid.text()
            customerType = ui.cb_customerType.currentText()
            
            if first == "" and last == "":
                islem.execute("update customer set customerType=? where cardid=?",(customerType,cardid))
            elif first == "" and customerType == "":
                islem.execute("update customer set lastName=? where cardid=?",(last,cardid))
            elif last == "" and customerType == "":
                islem.execute("update customer set firstName=? where cardid=?",(first,cardid))    
            else:
                islem.execute("update customer set firstName=?,lastName=?,customerType=? where cardid=?",(first,last,customerType,cardid))
                
            conn.commit()
            showCustomers()
            ui.statusbar.showMessage("Müşteri Kaydı Başarı ile Güncellendi.",10000)
            showCustomers()
        except Exception as error:
            ui.statusbar.showMessage("Başarısız!!! Müşteri Kaydı Güncellenemedi." + str(error))
    else:
        ui.statusbar.showMessage("Güncelleme işlemi iptal edildi.",10000)

def getSelected():
    row = ui.tableWidget.currentRow()
    first = ui.tableWidget.model().data(ui.tableWidget.model().index(row, 0))
    last = ui.tableWidget.model().data(ui.tableWidget.model().index(row, 1))
    cardid = ui.tableWidget.model().data(ui.tableWidget.model().index(row, 2))
    customerType = ui.tableWidget.model().data(ui.tableWidget.model().index(row, 3))
    if customerType == "Kamu":
        customerType = 0
    elif customerType == "Öğrenci":
        customerType = 1
    elif customerType == "Kamu Dışı":
        customerType = 2
    else:
        customerType = 0
    ui.lne_first.setText(first)
    ui.lne_last.setText(last)
    ui.lne_cardid.setText(cardid)
    ui.cb_customerType.setCurrentIndex(customerType)

def updateCustomerCount():
    update_msg = QMessageBox.question(window,"Güncelleme Onayı","Seçili müşteriye yemek hakkı vermek istediğinizden emin misiniz?",QMessageBox.Yes | QMessageBox.No)
    if update_msg == QMessageBox.Yes:
        try:
            cardid = ui.lne_cardid.text()
            islem.execute("update customer set count=? where cardid=?",(1,cardid))
            conn.commit()
            showCustomers()
            ui.statusbar.showMessage("Müşteri Kaydı Başarı ile Güncellendi.",10000)
        except Exception as error:
            ui.statusbar.showMessage("Başarısız!!! Müşteri Kaydı Güncellenemedi." + str(error))
    else:
        ui.statusbar.showMessage("Güncelleme işlemi iptal edildi.",10000)

def readCardID():
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

import os

def startTurnikeControl():
    os.system('python mainTurnike.py')
    

# Second Window
import serial.tools.list_ports
import serial

ser = serial.Serial()

def listPorts():
    ports = serial.tools.list_ports.comports()
    secUi.comList.clear()
    for port, desc, hwis in sorted(ports):
        secUi.comList.addItem(str(port+" "+desc))
    
def selectPort():
    global ser
    ser.close()
    portStr = secUi.comList.selectedItems()
    portStr = portStr[0].text()
    port = int(portStr[3:4:1])
    
    try:
        ser = serial.Serial(port='COM%d' % (int(port)), baudrate = 9600,  bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0)
        secUi.statusbar.showMessage("Başarılı bir şekilde bağlantı sağlandı.",5000)
    except Exception as error:
        secUi.statusbar.showMessage("Başarısız!!! Bağlantı sağlanamadı." + str(error))
    
        
        

def secWindow():
    secUi.setupUi(window_Com)
    window_Com.show()
    listPorts()
    
    secUi.btn_reflesh.clicked.connect(listPorts)
    secUi.btn_choose.clicked.connect(selectPort)

# Butonlar

ui.btn_add.clicked.connect(addCustomer)
ui.btn_unfilter.clicked.connect(showCustomers)
ui.btn_filter.clicked.connect(cusTypeFilter)
ui.btn_remove.clicked.connect(removeCustomer)
ui.btn_update.clicked.connect(updateCustomer)
ui.addCom.triggered.connect(secWindow)
ui.btn_read.clicked.connect(readCardID)
ui.btn_getSelected.clicked.connect(getSelected)
ui.btn_update_count.clicked.connect(updateCustomerCount)
ui.btn_startTurnike.clicked.connect(startTurnikeControl)

showCustomers()

sys.exit(app.exec_())