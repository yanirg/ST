
import urllib.request, json, time, sys
import csv
years=5

class Reporter(object):
    targetFile=None
    def __init__(self, fileName):
      self.targetFile=open(fileName,'a')


#C:\Users\yanirgo\Desktop\ST.csv
def readFromCsv(csvFile):
    stockList=None
    try:
        with open(csvFile,'r') as stockFile:
            stockList= list(csv.reader(stockFile, delimiter=','))
            #print (stockList) 
    except:
        sys.exit("fail to read CSV file")
    return  stockList  


class Stock(object):
    profile=[]
    dataSheet=[]
    incomes=[]
    cashFlow=[]
    keyMetrics=[]
    def __init__(self,name):
      self.sName=name



def gerProfile(comp):
    url = "https://financialmodelingprep.com/api/v3/company/profile/"+comp
    return getResponse(url, 'profile')

def gerCompanyKeyMetrics(comp, iPeriod):
    url = "https://financialmodelingprep.com/api/v3/company-key-metrics/"+comp
    mVal=getResponse(url,'metrics')
    return (mVal[0:iPeriod+1]) 

def gerBalanceSheetData(comp, iPeriod):
    url = "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/"+comp
    mVal=getResponse(url,'financials')
    return (mVal[0:iPeriod+1]) 


def getIncomes(comp, iPeriod):
    url = "https://financialmodelingprep.com/api/v3/financials/income-statement/"+ comp
    mVal=getResponse(url, 'financials')
    return (mVal[0:iPeriod+1]) 


def getCashFlow(comp, iPeriod):
    url = "https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/" + comp
    mVal=getResponse(url , 'financials')
    return (mVal[0:iPeriod+1])


def getResponse(url, section1):
    rslt = None
    with urllib.request.urlopen(url) as operUrl:
        if (operUrl.getcode() == 200):
            data = json.loads(operUrl.read())
            if section1 in data:
                ##print (data['financials'])
                rslt = data[section1]
        else:
            print("Error receiving data", operUrl.getcode())
        return rslt


def calcRate(currentRate, initialRate,  years):
    if (float(initialRate)==0):
        return 0
    return round((((float(currentRate)) / (float(initialRate)))**(1 / years) - 1).real,
                 2)  #cagr=(1980.0/1000)**(1/6.0)-1


def verifyPeriod(comp,iPeriod):
  url = "https://financialmodelingprep.com/api/v3/financials/income-statement/"+ comp
  mIncomes=getResponse(url,'financials')
  if type(mIncomes) == list:
    if len(mIncomes) >= iPeriod: 
      return True #(mIncomes[0:iPeriod+1])   
    else :
      print("return short period: "+str(len(mIncomes)))
  return False

def printStckValues(arg):
  if type(arg)==list:
    for i in range (0,len(arg)):
            print(i, arg[i]['date'], arg[i]['EPS']) 



cStockList=readFromCsv('C:\\\\Users\\MERAV\\Downloads\\ST.csv')
for i in cStockList:
    if (not verifyPeriod(i[0],years)):
       break
      #sys.exit("Stop Running")
    cStock=Stock(i[0])
    cStock.profile=gerProfile(cStock.sName)
    cStock.incomes=getIncomes(cStock.sName,years)
    cStock.cashFlow=getCashFlow(cStock.sName,years)
    cStock.dataSheet=gerBalanceSheetData(cStock.sName,years)
    cStock.keyMetrics= gerCompanyKeyMetrics(cStock.sName,years)

    EPSRate=calcRate(cStock.incomes[0]['EPS'], cStock.incomes[years]['EPS'], years)
    NetIncomesRate=calcRate(cStock.incomes[0]['Net Income'], cStock.incomes[years]['Net Income'], years)
    Totalequity=calcRate(cStock.dataSheet[0]['Total shareholders equity'], cStock.dataSheet[years]['Total shareholders equity'], years)
    OperatingCashFlow= calcRate(cStock.cashFlow[0]['Operating Cash Flow'], cStock.cashFlow[years]['Operating Cash Flow'], years)


    #printStckValues(cStock.incomes)
    print('companyName:'+cStock.profile['companyName']+' symbol:'+cStock.sName)
    print("EPS rate in "+str(years)+" :"+str(EPSRate*100)+"%")
    print("Net Income rate in "+str(years)+" :"+str(NetIncomesRate*100)+"%")
    print("Total shareholders equity in "+str(years)+" :"+str(Totalequity*100)+"%")
    print("Operating Cash Flow in "+str(years)+" :"+str(OperatingCashFlow*100)+"%")
    print("ROIC  "+cStock.keyMetrics[0]['ROIC'])
    print("currnet PE  "+cStock.keyMetrics[0]['PE ratio'])



time.sleep(1)




