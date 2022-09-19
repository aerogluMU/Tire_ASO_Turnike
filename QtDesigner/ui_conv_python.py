from PyQt5 import uic

with open("tireaso.py","w",encoding="utf-8") as fout:
    uic.compileUi("tireaso_qt.ui",fout)