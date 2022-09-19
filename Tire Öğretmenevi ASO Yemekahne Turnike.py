''' 
*
* LIBRARIES
*
'''

from threading import Thread
import threading
import serial.tools.list_ports
import serial
import sqlite3
from customer import Customer
import threading

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

# DATABASE FUNCTIONS

def insert_cus(cus):
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO customers VALUES (:first, :last, :cardID, 0)", {'first':cus.firstName,'last':cus.lastName,'cardID':cus.cardID})
    conn.close()

def get_cus_by_name(firstName,lastName):
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE firstName=:first AND lastName=:last",{'first':firstName, 'last':lastName})
    conn.close()
    return c.fetchall()

def get_cus_by_name(cardID):
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE cardID=:cardID",{'cardID':cardID})
    conn.close()
    return c.fetchone()

def countUsed(cardID):
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()
    with conn:
        c.execute("UPDATE customers SET count=0 WHERE cardID=:cardID",{'cardID':cardID})
    conn.close()

def countReflesh(cardID):
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()
    with conn:
        c.execute("UPDATE customers SET count=1 WHERE cardID=:cardID",{'cardID':cardID})
    conn.close()

def update_cardID(cus,newCardID):
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()
    with conn:
        c.execute("UPDATE customers SET cardID=:cardID WHERE firstName=:first AND lastName=:last",{'cardID':newCardID,'first':cus.firstName, 'last':cus.lastName})
    conn.close()

def remove_by_cardID(cus):
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()
    with conn:
        c.execute("DELETE from customers WHERE cardID=:cardID",{'cardID':cus.cardID})
    conn.close()

# THREAD FUNCTIONS

def Thread1():
    while 1:
        rxbuf = ""
        while 1:
            res = ser.read().decode("utf-8")
            if(res != '\n'):
                rxbuf += res
            else:
                print(">> ID: " + rxbuf)
                break

def Thread2():
    while 1:
        choose = input()
        if choose == "ekle":
            first = input("Ad: ")
            last = input("SoyAd: ")
            cardid = input("cardId: ")
            cus = Customer(firstName=first,lastName=last,cardID=cardid)
            insert_cus(cus)
        elif choose == "sil":
            cardid = input("cardId: ")
            cus = get_cus_by_name(cardid)
            remove_by_cardID(cus)
            

''' 
*
* MAIN
*
'''

# c.execute("""CREATE TABLE customers (
#             firstName text,
#             lastName text,
#             cardID text,
#             count integer
#             )""")


listandSelectPorts()
com=input('>> Select COM Port: COM')
ser = serial.Serial(port='COM%d' % (int(com)), baudrate = 9600,  bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0)
print("-------------------------------------------------------")

thread1 = threading.Thread(target=Thread1)
thread1.start()
thread2 = threading.Thread(target=Thread2)
thread2.start()