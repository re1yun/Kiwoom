import sys
from PyQt5.QtWidgets import *
from pykiwoom import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.kiwoom = Kiwoom()
        self.kiwoom.CommConnect()

        self.kiwoom.GetConditionLoad()
        conditions = self.kiwoom.GetConditionNameList()

        condition_index = conditions[0].split('^')[0]
        condition_name = conditions[0].split('^')[1]

        self.kiwoom.SendCondition("0101", condition_name, condition_index, 0)

        print("종목코드", "종목명")
        stock_list = get_stock_list()
        for code in stock_list:
            print(code)


        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()