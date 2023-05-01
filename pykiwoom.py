from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

global stock_list
stock_list = []

class Kiwoom:
    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.OnEventConnect)
        self.ocx.OnReceiveConditionVer.connect(self.OnReceiveConditionVer)
        self.ocx.OnReceiveTrCondition.connect(self.OnReceiveTRCondition)
        self.ocx.OnReceiveRealCondition.connect(self.OnReceiveRealCondition)

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

    def OnReceiveRealCondition(self, code, event, condition_name, condition_index):
        print("OnReceiveRealCondition", code, event, condition_name, condition_index)

def get_stock_list():
    return stock_list
