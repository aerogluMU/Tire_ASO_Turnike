''' 
*
* LIBRARIES
*
'''

import serial.tools.list_ports
import serial
import sqlite3
from customer import Customer

''' 
*
* FUNCTIONS
*
'''

# ARDUINO FUNCTIONS

def listandSelectPorts():
    ports = serial.tools.list_ports.comports()
    print("\n                    Tire ASO                \n")
    print("                    COM Port List             \n")
    print("Port Number | Port Name                               ")
    print("-------------------------------------------------------")
    for port, desc, hwis in sorted(ports):
            print("{} | {}".format(port, desc))

def readID():
    rxbuf = ""
    while 1:
        res = ser.read().decode("utf-8")
        if(res != '\n'):
            rxbuf += res
        else:
            print(rxbuf)
            break

# DATABASE FUNCTIONS

def insert_cus(cus):
    with conn:
        c.execute("INSERT INTO customers VALUES (:first, :last, :cardID, 0)", {'first':cus.firstName,'last':cus.lastName,'cardID':cus.cardID})

def get_cus_by_name(lastName):
    c.execute("SELECT * FROM customers WHERE lastName=:last",{'last':lastName})
    return c.fetchall()

def update_count(cus):
    with conn:
        c.execute("SELECT * FROM customers WHERE lastName=:last",{'last':lastName})


''' 
*
* MAIN
*
'''

conn = sqlite3.connect('customer.db')

c = conn.cursor()

# c.execute("""CREATE TABLE customers (
#             firstName text,
#             lastName text,
#             cardID text,
#             count integer
#             )""")


conn.close()

listandSelectPorts()
com=input('>> Select COM Port: COM')
ser = serial.Serial(port='COM%d' % (int(com)), baudrate = 9600,  bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0)
print("-------------------------------------------------------")
while 1:
    readID()


