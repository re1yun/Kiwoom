import sys
from PyQt5.QtWidgets import *
from pykiwoom import *
import time

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.kiwoom = Kiwoom()
        self.kiwoom.CommConnect()

        self.kiwoom.GetConditionLoad()
        conditions = self.kiwoom.GetConditionNameList()

        condition_index = conditions[0].split('^')[0]
        condition_name = conditions[0].split('^')[1]

        #name = "단타매매", index = 000
        self.kiwoom.SendCondition("0101", condition_name, condition_index, 0)

        print("종목코드", "종목명")
        stock_list = self.kiwoom.get_stock_list()
        for code in stock_list:
            self.kiwoom.Get2Resistance(code[0])
            print(code[0], code[1])
            time.sleep(0.5)
        stock_data = self.kiwoom.get_stock_data()
        print("printing stock data")
        for data in stock_data:
            print(data["code"], data["date"], data["high_price"], data["close_price"], data["r2"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()