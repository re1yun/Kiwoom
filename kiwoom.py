from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

account_num = kiwoom.GetLoginInfo("ACCOUNT_CNT")
accounts = kiwoom.GetLoginInfo("ACCNO")
user_id = kiwoom.GetLoginInfo("USER_ID")
user_name = kiwoom.GetLoginInfo("USER_NAME")
keyboard = kiwoom.GetLoginInfo("KEY_BSECGB")
firewall = kiwoom.GetLoginInfo("FIREW_SECGB")

print("내 정보")
print()
print("계좌 갯수: ", account_num)
print("내 계좌 번호: ", accounts)
print("내 유저 ID: ", user_id)
print("내 이름: ", user_name)

print()

kospi = kiwoom.GetCodeListByMarket('0')
kosdaq = kiwoom.GetCodeListByMarket('10')
etf = kiwoom.GetCodeListByMarket('8')

print(len(kospi), len(kosdaq), len(etf))
print(kospi[:5])

print()

# GetMasterCodeName은 종목코드를 입력하면 종목명을 반환한다.
name = kiwoom.GetMasterCodeName("005930")

# GetConnectState는 현재 접속 상태를 반환한다. 0이면 미접속, 1이면 접속 상태이다.
state = kiwoom.GetConnectState()

# GetMasterListedStockCnt는 특정 종목의 상장주식수를 반환한다.
stock_cnt = kiwoom.GetMasterListedStockCnt("005930")
print(name, "의 주식수는: ", stock_cnt)

# GetMasterConstruction은 특정 종목의 감리구분을 반환한다. 1이면 정상, 0이면 투자유의, 2이면 투자경고, 3이면 투자위험, 4이면 투자주의이다.
감리구분 = kiwoom.GetMasterConstruction("005930")

# GetMasterLastPrice는 특정 종목의 전일종가를 반환한다.
전일가 = kiwoom.GetMasterLastPrice("005930")

# 현재가 기준 시가 총액 50식억원 이상 2000십억원 이하
# pivot 0봉전 종가 >= 2차 저항
# pivot 0붕전 시가 < 2차 저항
# 거래대금 500이상 99999999이하
# 주가비교: 1봉전 종가 <= 0봉전 저가
# 거래대금 순위 상위 150위
