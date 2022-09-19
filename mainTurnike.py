import sqlite3
from tabnanny import check
import serial.tools.list_ports
import serial

# FUNCTIONS

def checkCustomerCount(cardid):
    islem.execute("SELECT * FROM customer WHERE cardid=?",(cardid,))
    cus = islem.fetchone()
    return cus[4]

def updateCustomerCount(cardid):
    try:
        islem.execute("update customer set count=? where cardid=?",(0,cardid))
        conn.commit()
        print(">> Basarili!!!")
    except Exception as error:
        print(">> Basarisiz!!! "+str(error))

def listandSelectPorts():
    ports = serial.tools.list_ports.comports()
    print("\n                    Tire ASO                \n")
    print("                    COM Port List             \n")
    print("Port Number | Port Name                               ")
    print("-------------------------------------------------------")
    for port, desc, hwis in sorted(ports):
            print("{} | {}".format(port.encode('utf-8'), desc.encode('utf-8')))

# MAIN
conn = sqlite3.connect("customers.db")

islem = conn.cursor()
conn.commit()

listandSelectPorts()

com=input('>> COM Port secin: COM')
ser = serial.Serial(port='COM%d' % (int(com)), baudrate = 9600,  bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0)
print("-------------------------------------------------------")
while 1:
    rxbuf = ""
    while 1:
        res = ser.read().decode("utf-8")
        if(res != '\n'):
            rxbuf += res
        else:
            if(checkCustomerCount(rxbuf)):
                updateCustomerCount(rxbuf)
            else:
                print(">> Yemek hakki yoktur.")
            break
