#c3n8e02ad3ieepc46grg
from tkinter import *
from tkinter import filedialog
import json
import requests
import csv
import os
import shutil
from datetime import datetime
from datetime import date
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import pandas as pd
watchFile = open('watchfile.csv','r')

def runProgram():    

    
    #resetting view
    stockNames.grid_forget()
    stockNames.delete(0, END)
    negStocks.grid_forget()
    negCross.grid_forget()
    border3.grid_forget()
    rP_border3.grid_forget()
    resolutionList.grid_forget()
    r1.grid_forget()
    r2.grid_forget()

    #Getting stock List
    global stockListFile
    try:
        stockListFile = open('customListOfStocks.csv')
    except:
        stockListFile = open('listOfStocks.csv')
        
    csvStockList = csv.reader(stockListFile)

    stockList = list()
    for stock in csvStockList:
        stockList.append(stock[0])

    #opening last time list
    watchFile = open('watchfile.csv','a', newline = '')
    csvWriter = csv.writer(watchFile)
        
    if radioChoice.get() == 1:            
        #get ema
        for stock in stockList:

            res, short, long = str(), int(), int()
            if resolution.get() == 'Day':
                res, short, long = 'D', 10, 21
            elif resolution.get() == '4 hours':
                res, short, long = '60', 40, 84
            elif resolution.get() == '2 hours':
                res, short, long = '60', 20, 42
            elif resolution.get() == 'Week':
                res, short, long = 'W', 10, 21
            else:
                res, short, long = 'D', 10, 21
                
            stockEMA = getEMA(stock,res,short,long)
            counter = 0
            while len(stockEMA[0]) == 1 or len(stockEMA[1]) == 1:
                print('.') #RID
                counter += 1
                if counter > 10:
                    break
                stockEMA = getEMA(stock,res,short,long)
                
            if counter > 10:
                continue

            if stockEMA[0]['ema'][-2] < stockEMA[1]['ema'][-2] and stockEMA[0]['ema'][-1] > stockEMA[1]['ema'][-1]:
                print(stock + ' - Yes')
                csvWriter.writerow([stock])
                stockNames.insert(END, stock)
                '''
                #get eps
                stockEPS = getEPS(stock)
                while len(stockEPS) == 1:
                    print('*') #RID
                    stockEPS = getEPS(stock)

                
                i = 0
                while stockEPS[i]['actual'] == None:
                    i += 1
                '''
                '''
                if stockEPS[0]['reportedEPS'] > stockEPS[0]['estimatedEPS'] and stockEPS[1]['reportedEPS'] > stockEPS[1]['estimatedEPS']:
                    #get Revenue
                    stockRevenue = getRevenue(stock)
                    if stockRevenue[0]['totalRevenue'] > stockRevenue[1]['totalRevenue'] and stockRevenue[1]['totalRevenue'] > stockRevenue[2]['totalRevenue']:

                        stockRSI = getRSI(stock, 14)
                        if stockRSI[-3] < stockRSI[-2] and stockRSI[-2] < stockRSI[-1]: 
                            print(stock + ' - Yes')
                            csvWriter.writerow([stock])
                            stockNames.insert(END, stock)

                        else:
                            print(stock + ' - No(d)')

                    else:
                        print(stock + ' - No(c)')
                        
                else:
                    print(stock + ' - No(b)')
                '''
            else:
                print(stock + ' - No(a)')

    elif radioChoice.get() == 2:

        for stock in stockList:
            
            #get ema
            stockEMA = getEMA(stock,'D', 10, 21)
            counter = 0
            print('new stock')
            while len(stockEMA[0]) == 1 or len(stockEMA[1]) == 1:
                print('.') #RID
                counter += 1
                if counter > 10:
                    print('counter check in while loop done')#RID
                    break
                try:
                    stockEMA = getEMA(stock,'D',10,21)
                except:
                    break
                
            if counter > 10 or (len(stockEMA[0]) == 1 or len(stockEMA[1]) == 1):
                print('counter check outside while loop done')#RID
                continue
            
            if stockEMA[0]['ema'][-4] < stockEMA[1]['ema'][-4] and stockEMA[0]['ema'][-3] > stockEMA[1]['ema'][-3]:
            
                #get ppo
                stockPPO = getPPO(stock)
                try:
                    if stockPPO[-2] > 0 and stockPPO[-1] > 0:

                        if isGreenCandle(stock):

                            stockRSI = getRSI(stock, 14)
                            if stockRSI[-3] > 50 and stockRSI[-2] > 50 and stockRSI[-1] > 50:
                                #get eps
                                stockEPS = getEPS(stock)
                                if len(stockEPS) == 0:
                                    print(stock + ' - No(EPS)')
                                    continue   
                                
                                if float(stockEPS[0]['reportedEPS']) > 0 and float(stockEPS[1]['reportedEPS'] > 0):

                                    stockRevenue = getRevenue(stock)
                                    if len(stockRevenue) == 0:
                                        print(stock + ' - No(Revenue)')
                                        continue

                                    if float(stockRevenue[0]['totalRevenue']) > float(stockRevenue[1]['totalRevenue']):

                                        print(stock + ' - Yes')
                                        csvWriter.writerow([stock])
                                        stockNames.insert(END, stock)
                                        
                                    else:
                                        print(stock + ' - No(Revenue)')    
                                else:
                                    print(stock + ' - No(EPS)')  
                            else:
                                print(stock + ' - No(RSI)')    
                            
                        else:
                            print(stock + ' - No(GreenCandle)')
                        
                    else:
                        print(stock + ' - No(PPO)')
                except:
                    print(stock + ' - No(PPO)')
                
            else:
                print(stock + ' - No(EMA)')            
            
    stockNames.grid(row = 1, column = 0, padx = 150, pady = 20, columnspan = 2)
    rP_border4.grid(row = 2, column = 0, padx = 25, pady = 0, columnspan = 2)

    watchFile.close()   
    

deletedStockList = list()
def deleteStocks():
    global watchFile
    global stocks
    global deletedStockList
    watchFile.close()
    watchFile = open('watchfile.csv', 'w', newline = '')
    csvWriter = csv.writer(watchFile)
  
    if len(negStocks.curselection()) >= 1:
        tempStocks = stocks.copy()
        for stock in tempStocks:
            isDeleted = False
            for i in negStocks.curselection():
                if stock == negStocks.get(i):
                    negStocks.delete(i)
                    isDeleted = True
                    if stock not in deletedStockList:
                        stocks.remove(stock)
                        deletedStockList.append(stock)
                    break
                
            if not isDeleted:
                csvWriter.writerow([stock])
                
    if len(stockNames.curselection()) >= 1:
        tempStocks = stocks.copy()
        for stock in tempStocks:
            isDeleted = False
            for i in stockNames.curselection():
                if stock == stockNames.get(i):
                    stockNames.delete(i)
                    isDeleted = True
                    if stock not in deletedStockList:
                        stocks.remove(stock)
                        deletedStockList.append(stock)
                    break

            if not isDeleted:
                csvWriter.writerow([stock])
        
    watchFile.close()

def displayCurrStocks():    
    global watchFile    
    try:
        shutil.copy(os.getcwd() + '/customListOfStocks.csv', os.getcwd() + '/watchfile.csv')
        watchFile = open('watchfile.csv','r')
    except:
        watchFile = open('watchfile.csv','r')   
 
    stockNames.grid_forget()
    stockNames.delete(0, END)
    negStocks.delete(0,END)
    resolutionList.grid_forget()
    rP_border3.grid_forget()
    r1.grid_forget()
    r2.grid_forget()

    
    global stocks
    csvStocks = csv.reader(watchFile)

    stocks = list()
    for csvstock in csvStocks:
        stocks.append(csvstock[0])
        stockNames.insert(END, csvstock[0])
   
    #stock names
    stockNames.grid(row = 2, column = 0, padx = 25, pady = 20, rowspan = 2, sticky = NE)

    negCross.grid(row = 1, column = 1, pady = 10, sticky = W)

    #stocks no longer ema
    for stock in stocks:

        res, short, long = str(), int(), int()
        if resolution.get() == 'Day':
            res, short, long = 'D', 5, 12
        elif resolution.get() == '4 hours':
            res, short, long = '60', 20, 48
        elif resolution.get() == '2 hours':
            res, short, long = '60', 10, 24
        elif resolution.get() == 'Week':
            res, short, long = 'W', 5, 12
        else:
            res, short, long = 'D', 5, 12
            
        print(stock)
        stockEMA = getEMA(stock, res, short, long)
        
        counter = 0
        while len(stockEMA[0]) == 1 or len(stockEMA[1]) == 1:
            print('.') #RID
            counter += 1
            if counter > 10:
                break
            stockEMA = getEMA(stock, res, short, long)
        if counter > 10:
            continue
        
        if stockEMA[0]['ema'][-2] > stockEMA[1]['ema'][-2] and stockEMA[0]['ema'][-1] < stockEMA[1]['ema'][-1]:
            negStocks.insert(END, stock)
            
    negStocks.grid(row = 2, column = 1, padx = 25, pady = 10, sticky = W)

    border3.grid(row = 3, column = 1, padx = 25, pady = 20)

    rP_border4.grid(row = 4, column = 0, padx = 25, pady = 0)
    
    watchFile.close()

def getEMA(stock, resolution, shortC, longC):
    #past 1 year
    toTime = datetime.now()
    toTime = int(toTime.timestamp())

    fromTime = toTime - 31104000
    fromTime = str(fromTime)
    toTime = str(toTime)

    #request
    requestLinkPart1 = 'https://finnhub.io/api/v1/indicator?symbol='
    requestLinkPart2 = '&resolution='
    requestLinkPart3 = '&from='
    requestLinkPart4 = '&to='
    requestLinkPart5 = '&indicator=ema&timeperiod='
    requestLinkPart6 = '&seriestype=c&token=c3n8e02ad3ieepc46grg'
    
    #ema short
    requestLink = requestLinkPart1 + stock + requestLinkPart2 + resolution + requestLinkPart3 + fromTime + requestLinkPart4 + toTime + requestLinkPart5 + str(shortC) + requestLinkPart6
    r = requests.get(requestLink)
    stockPriceDetailsS = r.json()

    #ema long
    requestLink = requestLinkPart1 + stock + requestLinkPart2 + resolution + requestLinkPart3 + fromTime + requestLinkPart4 + toTime + requestLinkPart5 + str(longC) + requestLinkPart6
    r = requests.get(requestLink)
    stockPriceDetailsL = r.json()

    #print(stockPriceDetails5['ema'][-1])

    return stockPriceDetailsS, stockPriceDetailsL   

def getEMAgraph(self):
    #past 2 months
    toTime = datetime.now()
    toTime = int(toTime.timestamp())

    fromTime = toTime - 5184000
    fromTime = str(fromTime)
    toTime = str(toTime)

    #which stock to generate graph for
    stock = self.widget.get(self.widget.curselection())
    
    requestLinkPart1 = 'https://finnhub.io/api/v1/indicator?symbol='
    requestLinkPart2 = '&resolution=D&from='
    requestLinkPart3 = '&to='
    requestLinkPart4 = '&indicator=ema&timeperiod=5&seriestype=c&token=c3n8e02ad3ieepc46grg'
    requestLinkPart4p5 = '&indicator=ema&timeperiod=12&seriestype=c&token=c3n8e02ad3ieepc46grg'

    #ema short
    requestLink = requestLinkPart1 + stock + requestLinkPart2 + fromTime + requestLinkPart3 + toTime + requestLinkPart4
    r = requests.get(requestLink)
    stockPriceDetails5 = r.json()

    #ema long
    requestLink = requestLinkPart1 + stock + requestLinkPart2 + fromTime + requestLinkPart3 + toTime + requestLinkPart4p5
    r = requests.get(requestLink)
    stockPriceDetails12 = r.json()

    #timestamp to actual date
    for i in range(len(stockPriceDetails5['t'])):
        stockPriceDetails5['t'][i] = datetime.fromtimestamp(stockPriceDetails5['t'][i])

    stockTimes5 = dates.date2num(stockPriceDetails5['t'])

    for i in range(len(stockPriceDetails12['t'])):
        stockPriceDetails12['t'][i] = datetime.fromtimestamp(stockPriceDetails12['t'][i])
    
    stockTimes12 = dates.date2num(stockPriceDetails12['t'])

    #plotting
    plt.plot_date(stockTimes5, stockPriceDetails5['ema'], 'r')
    plt.plot_date(stockTimes12, stockPriceDetails12['ema'], 'g')
    plt.show()

def getEPS(stock):
    requestLinkPart1 = 'https://www.alphavantage.co/query?function=EARNINGS&symbol='
    requestLinkPart2 = '&apikey=KGFO1XW9K53AE4NQ'

    requestLink = requestLinkPart1 + stock + requestLinkPart2
    r = requests.get(requestLink)
    EPSdetails = r.json()

    try:
        return EPSdetails['quarterlyEarnings']
    except:
        return EPSdetails

def getRevenue(stock):
    #past 1 yr
    #KGFO1XW9K53AE4NQ
    requestLinkPart1 = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='
    requestLinkPart2 = '&apikey=KGFO1XW9K53AE4NQ'

    requestLink = requestLinkPart1 + stock + requestLinkPart2
    r = requests.get(requestLink)
    stockIncomes = r.json()

    try:
        return stockIncomes['quarterlyReports']
    except:
        return stockIncomes

def customRun():
    main.filename = filedialog.askopenfilename(title = 'Select a List', filetypes = (('Excel files','*.xlsx'),('Comma Seperated Value','*.csv')))

    if main.filename == '':
        return

    global stockListFile
    if main.filename.find('.xlsx') != -1:
        stockListFile = pd.read_excel(main.filename)
        stockListFile.to_csv(os.getcwd() + '/customListOfStocks.csv', index = False)
    else:
        shutil.copy(main.filename, os.getcwd() + '/customListOfStocks.csv')

    stockListFile = open('customListOfStocks.csv')

def getPPO(stock):
    
    #past 1 year
    toTime = datetime.now()
    toTime = int(toTime.timestamp())

    fromTime = toTime - 31104000
    fromTime = str(fromTime)
    toTime = str(toTime)

    #request
    requestLinkPart1 = 'https://finnhub.io/api/v1/indicator?symbol='
    requestLinkPart2 = '&resolution=D&from='
    requestLinkPart3 = '&to='
    requestLinkPart4 = '&indicator=ppo&fastperiod=1&slowperiod=21&seriestype=c&token=c3n8e02ad3ieepc46grg'
    
    #ema short
    requestLink = requestLinkPart1 + stock + requestLinkPart2 + fromTime + requestLinkPart3 + toTime + requestLinkPart4
    r = requests.get(requestLink)
    stockPPO = r.json()
    
    try:
        return stockPPO['ppo']       
    except:
        return stockPPO

def isGreenCandle(stock):

    #past 1 year
    toTime = datetime.now()
    toTime = int(toTime.timestamp())

    fromTime = toTime - 31104000
    fromTime = str(fromTime)
    toTime = str(toTime)

    #request
    requestLinkPart1 = 'https://finnhub.io/api/v1/stock/candle?symbol='
    requestLinkPart2 = '&resolution=D&from='
    requestLinkPart3 = '&to='
    requestLinkPart4 = '&token=c3n8e02ad3ieepc46grg'

    requestLink = requestLinkPart1 + stock + requestLinkPart2 + fromTime + requestLinkPart3 + toTime + requestLinkPart4
    r = requests.get(requestLink)
    stockCandles = r.json()
   
    try:
        return (stockCandles['c'][-2] > stockCandles['o'][-2] and stockCandles['c'][-1] > stockCandles['o'][-1])
    except:
        return False
    
    
'''
def timeSet():
    global toTime, fromTime

    toTime = datetime.now()
    toTime = int(toTime.timestamp())

    fromTime = toTime - 345600
    fromTime = str(fromTime)
    toTime = str(toTime)

#get stock prices of past 4 days
def getStockPrices():
    timeSet()
    
    requestLinkPart1 = 'https://finnhub.io/api/v1/stock/candle?symbol='
    stock = 'AAPL'
    requestLinkPart2 = '&resolution=D&from='
    requestLinkPart3 = '&to='
    requestLinkPart4 = '&token=c3n8e02ad3ieepc46grg'

    requestLink = requestLinkPart1 + stock + requestLinkPart2 + fromTime + requestLinkPart3 + toTime + requestLinkPart4
    r = requests.get(requestLink)
    stockPriceDetails = r.json()
'''

def getRSI(stock, tPeriod):
    toTime = datetime.now()
    toTime = int(toTime.timestamp())

    fromTime = toTime - 31104000
    fromTime = str(fromTime)
    toTime = str(toTime)
    
    requestLinkPart1 = 'https://finnhub.io/api/v1/indicator?symbol='
    requestLinkPart2 = '&resolution=D&from='
    requestLinkPart3 = '&to='
    requestLinkPart4 = '&indicator=rsi&timeperiod='
    requestLinkPart5 = '&seriestype=c&token=c3n8e02ad3ieepc46grg'

    requestLink = requestLinkPart1 + stock + requestLinkPart2 + fromTime + requestLinkPart3 + toTime + requestLinkPart4 + str(tPeriod) + requestLinkPart5
    r = requests.get(requestLink)
    stockPriceDetails = r.json()

    return stockPriceDetails['rsi']
    
    
def getADX(stock, tPeriod):
    toTime = datetime.now()
    toTime = int(toTime.timestamp())

    fromTime = toTime - 31104000
    fromTime = str(fromTime)
    toTime = str(toTime)
    
    requestLinkPart1 = 'https://finnhub.io/api/v1/indicator?symbol='
    requestLinkPart2 = '&resolution=D&from='
    requestLinkPart3 = '&to='
    requestLinkPart4 = '&indicator=adx&timeperiod='
    requestLinkPart5 = '&token=c3n8e02ad3ieepc46grg'

    requestLink = requestLinkPart1 + stock + requestLinkPart2 + fromTime + requestLinkPart3 + toTime + requestLinkPart4 + tPeriod + requestLinkPart5
    r = requests.get(requestLink)
    stockPriceDetails = r.json()

    return stockPriceDetails['adx']
'''
def getAD():
    toTime = datetime.now()
    toTime = int(toTime.timestamp())

    fromTime = toTime - 2592000
    fromTime = str(fromTime)
    toTime = str(toTime)
    
    requestLinkPart1 = 'https://finnhub.io/api/v1/indicator?symbol='
    stock = 'AAPL'
    requestLinkPart2 = '&resolution=D&from='
    requestLinkPart3 = '&to='
    requestLinkPart4 = '&indicator=adx&token=c3n8e02ad3ieepc46grg'

    requestLink = requestLinkPart1 + stock + requestLinkPart2 + fromTime + requestLinkPart3 + toTime + requestLinkPart4
    r = requests.get(requestLink)
    stockPriceDetails = r.json()
    print(stockPriceDetails['adx'])
'''
#back function
def Back():
    for widget in main.grid_slaves():
        widget.grid_forget()

    rP_border.grid(row = 0, column = 0, padx = (100,20), pady = 20, sticky = W)
    rP_border2.grid(row = 0, column = 1, padx = (20,100), pady = 20, sticky = E)
    rP_border3.grid(row = 1, column = 0, columnspan = 2, padx = 100, pady = 20)
    resolutionList.grid(row = 2, column = 0, columnspan = 2, padx = 100, pady = 20)
    
#building the GUI
main = Tk()
main.title('Stock Fetcher')
main.geometry('625x600')
main.configure(bg = 'white')

#stock names
global stockNames
stockNames = Listbox(main, bd  = 0, bg = 'white', fg = 'black', font = (None, 16), relief = FLAT, selectmode = EXTENDED)
stockNames.bind('<Double-1>', getEMAgraph)

#stock to delete list
global negStocks
negStocks = Listbox(main, bd  = 0, bg = 'white', fg = 'black', font = (None, 16), relief = FLAT, selectmode = EXTENDED)
negStocks.bind('<Double-1>', getEMAgraph)

#stocks to delete
global negCross
negCross = Label(main, text = 'Stocks with negative EMA cross:', bg = 'white', fg = 'black', font = (None, 16))

#delete button
global border3
border3 = LabelFrame(main, bd = 2, bg = 'black', relief = FLAT)
deleteButton = Button(border3, text = 'Delete Stocks', font = (None, 16), bd = 0, command = deleteStocks, bg = 'white').pack(ipady = 10)

#Run Program button
rP_border = LabelFrame(main, bd = 2, bg = 'black', relief = FLAT)
runProgramButton = Button(rP_border, text = 'Find new stocks', font = (None, 16), bd = 0, command = runProgram, bg = 'white').pack(ipady = 10)
rP_border.grid(row = 0, column = 0, padx = (100,20), pady = 20, sticky = W)

#check current stocks button
rP_border2 = LabelFrame(main, bd = 2, bg = 'black', relief = FLAT)
checkCurrButton = Button(rP_border2, text = 'Check Current Stocks', font = (None, 16), bd = 0, command = displayCurrStocks, bg = 'white').pack(ipady = 10)
rP_border2.grid(row = 0, column = 1, padx = (20,100), pady = 20, sticky = E)

#upload custom list
rP_border3 = LabelFrame(main, bd = 2, bg = 'black', relief = FLAT)
customListButton = Button(rP_border3, text = 'Upload custom list', font = (None, 16), bd = 0, command = customRun, bg = 'white').pack(ipady = 10)
rP_border3.grid(row = 1, column = 0, columnspan = 2, padx = 100, pady = 20)

#choose time frame
resolution = StringVar()
resolution.set('Select resolution')
resolutionList = OptionMenu(main, resolution, 'Day', '4 hours', '2 hours', 'Week')
resolutionList.config(background = 'white', activebackground = 'white', relief = FLAT, borderwidth = 2, activeforeground = 'black', highlightbackground = 'black', font = (None, 16))
resolutionList['menu'].config(background = 'white', activebackground = 'black', activeforeground = 'white', relief = FLAT, borderwidth = 2, font = (None, 16))
resolutionList.grid(row = 2, column = 0, columnspan = 2, padx = 100, pady = 20)

#back button
rP_border4 = LabelFrame(main, bd = 2, bg = 'black', relief = FLAT)
backButton = Button(rP_border4, text = 'Back', font = (None, 16), bd = 0, command = Back, bg = 'white').pack(ipady = 10, ipadx = 10)

#Method chooser radio button
radioChoice = IntVar() 
r1 = Radiobutton(main, text = 'EMA method', bg = 'white', font = (None, 16), variable = radioChoice, value = 1, indicator = 1)
r1.grid(row = 3, column = 0, padx = 50, pady = 20)
r2 = Radiobutton(main, text = 'DPO & RSI method', bg = 'white', font = (None, 16), variable = radioChoice, value = 2, indicator = 1)
r2.grid(row = 3, column = 1, padx = 50, pady = 20)

mainloop()





    
    
