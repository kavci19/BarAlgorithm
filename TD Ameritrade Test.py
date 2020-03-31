#!/usr/bin/env python
# coding: utf-8

# In[6]:


import requests
import time
from datetime import datetime
import winsound
from flask import Flask
from flask_mail import Mail, Message
import os
import smtplib
from plyer import notification


frequency = 200  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
#winsound.Beep(frequency, duration)

clientKey = 'ROXZBKOQYZKNQHTFGERLA5RLPN2LLHSZ'
endpoint = r"https://api.tdameritrade.com/v1/marketdata/quotes"


# In[7]:


notification.notify(
title = "Invest in /CLK20",
message = "Bar Algorithm predicts that this is a good entry point", 
timeout = 10)


# In[ ]:





# In[6]:


def retrieveStockQuote(stock):
    payload = {'apikey':clientKey,
                'symbol': stock}

    content = requests.get(url = endpoint, params = payload)

    data = content.json()
    stockQuote = data.get(stock)
    
    openPrice = stockQuote.get('openPriceInDouble')
    closePrice = stockQuote.get('closePriceInDouble')
    highPrice = stockQuote.get('highPriceInDouble')
    lowPrice = stockQuote.get('lowPriceInDouble')
    
    stockQuote = [openPrice, closePrice, highPrice, lowPrice]
    return stockQuote
    


# In[3]:


class stockID:
    
    def __init__(self, quote):
        
        self.open = quote[0]
        self.close = quote[1]
        self.high = quote[2]
        self.low = quote[3]
    
    def isUpward(self):
        
        return self.close > self.open
    
    def isDownward(self):
        
        return self.close < self.open
    
    def halfMark(self):
        
        return self.open + ((self.close - self.open)/2)
    
    def isQuarterGrowthPlus(self, previous):
        
        minGrowth = (previous.open - previous.close)/2 
        
        
        
        if (self.close >= previous.open + minGrowth):
            return True
        
        else:
            return False
    
    


# In[ ]:


quoteTwoMinutesAgo = stockID([0,0, 0,0])
quoteOneMinuteAgo = stockID([0,0, 0,0])
quoteCurrent = stockID([0,0,0,0])



buffer = 0.03

i = 0

while (True):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    
    quoteTwoMinutesAgo = quoteOneMinuteAgo
    quoteOneMinuteAgo = quoteCurrent
    quoteCurrent = stockID(retrieveStockQuote('/CLK20'))
    
    
    if (quoteTwoMinutesAgo.isUpward() and
        quoteOneMinuteAgo.isDownward() and
        quoteCurrent.isUpward()):

        if (quoteOneMinuteAgo.close >= quoteTwoMinutesAgo.halfMark()):

            
            if (quoteTwoMinutesAgo.close + buffer >= quoteOneMinuteAgo.open and
                quoteTwoMinutesAgo.close - buffer <= quoteOneMinuteAgo.open):
                
                if (quoteCurrent.open + buffer >= quoteOneMinuteAgo.close and
                    quoteCurrent.open - buffer <= quoteOneMinuteAgo.close):
                    
                    
                    if (quoteCurrent.isQuarterGrowthPlus(quoteOneMinuteAgo)):
                        
                        print('Buy now!')
                        #winsound.Beep(frequency, duration)
                        notification.notify(
                            title = "Invest in /CLK20",
                            message = "Bar Algorithm predicts that this is a good entry point", 
                            timeout = 10)

    
    
    print()
    time.sleep(60)
    
    


# In[ ]:




