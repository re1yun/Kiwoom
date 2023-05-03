from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

global stock_list, stock_data
stock_list = []
stock_data = []

class Kiwoom:
    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.OnEventConnect)
        self.ocx.OnReceiveConditionVer.connect(self.OnReceiveConditionVer)
        self.ocx.OnReceiveTrCondition.connect(self.OnReceiveTRCondition)
        self.ocx.OnReceiveRealCondition.connect(self.OnReceiveRealCondition)
        self.ocx.OnReceiveTrData.connect(self.OnReceiveTrData)

    def CommConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.login_loop = QEventLoop()
        self.login_loop.exec_()

    def OnEventConnect(self, err_code):
        if err_code == 0:
            print("Connected")
        else:
            print("Disconnected")
        self.login_loop.exit()
    
    def GetMasterCodeName(self, code):
        name = self.ocx.dynamicCall("GetMasterCodeName(QString)", code)
        return name

    def GetConditionNameList(self):
        data = self.ocx.dynamicCall("GetConditionNameList()")
        conditions = data.split(';')
        return conditions[:-1]
    
    def GetConditionNameListByIndex(self, index):
        data = self.ocx.dynamicCall("GetConditionNameListByIndex(int)", index)
        conditions = data.split(';')
        return conditions[:-1]
    
    def GetConditionLoad(self):
        self.ocx.dynamicCall("GetConditionLoad()")
        self.condition_loop = QEventLoop()
        self.condition_loop.exec_()

    def SendCondition(self, screen, condition_name, index, search):
        print("SendCondition", screen, condition_name, index, search)
        self.ocx.dynamicCall("SendCondition(QString, QString, int, int)", screen, condition_name, index, search)
        self.send_condition_loop = QEventLoop()
        self.send_condition_loop.exec_()

    def SendConditionStop(self, screen, condition_name, index):
        self.ocx.dynamicCall("SendConditionStop(QString, QString, int)", screen, condition_name, index)


    def OnReceiveConditionVer(self, ret, msg):
        print("OnReceiveConditionVer", ret, msg)
        self.condition_loop.exit()

    def OnReceiveTRCondition(self, screen, codeList, conditionName, index, next):
        if codeList == "":
            return
        codes = codeList.split(';')
        for code in codes[:-1]:
            name = self.GetMasterCodeName(code)
            stock_list.append([code, name])
        self.send_condition_loop.exit()

    def OnReceiveRealCondition(self, code, event, condition_name, condition_index):
        print("OnReceiveRealCondition", code, event, condition_name, condition_index)

    def get_stock_list(self):
        return stock_list

    def GetCommData(self, trcode, rqname, index, item):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, item)
        return data.strip()
    
    def Get2Resistance(self, code):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보요청", "opt10001", 0, "0101")
        self.tr_loop = QEventLoop()
        self.tr_loop.exec_()
        
    def OnReceiveTrData(self, screen, rq_name, tr_code, record_name, prev_next):
        if tr_code == "opt10001":
            print("OnReceiveTrData", screen, rq_name, tr_code, record_name, prev_next)
            high_price = self.GetCommData(tr_code, rq_name, 0, "고가")
            low_price = self.GetCommData(tr_code, rq_name, 0, "저가")
            close_price = self.GetCommData(tr_code, rq_name, 0, "현재가")
            stock_data.append({"high_price": high_price, "low_price": low_price, "close_price": close_price})
            self.tr_loop.exit()

    def GetCommData(self, trcode, rqname, index, item):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, item)
        data = data.strip()
        return int(data)
    
    def get_stock_data(self):
        print("return stock_data")
        return stock_data
            