# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 14:13:08 2017

@author: dkumar7
"""

#import date modules
import pandas as pd
from nsepy import get_history
from datetime import date
from pandas.tseries.offsets import BDay

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#notify function when called with a mail subject and body will send a mail to pre-def list of users
def notify(mailsub, mailbody):
    fromaddr = "kdeepu@gmail.com"
    #toaddr = ['netmaildeepak@gmail.com', 'Leslie.Joseph@gmail.com', 'Rohit_chauhan@yahoo.com']
    toaddr = ['netmaildeepak@gmail.com']
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    msg['Subject'] = mailsub
 
    body = str(mailbody)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "vW4AJPu7u1wk")
    text = msg.as_string()
    msg = "Notification mail via Python"
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    return

#notify Review checks if there is an event worth notifying
def notifyReview(df):
      
    df = df[df.review.str.contains("Reconsider|Review|Sell")]
    df = df.iloc[:,[2,3]]
    df.iloc[:,[0]] = df.iloc[:,[0]].apply(pd.Series.round)
    
    if not df.empty:
        if 'Sell' in df.values:
             emailSub = 'Alert: SELL NOW - 20% drop from peak'
             emailBody = df
             notify(emailSub, emailBody)
        elif 'Reconsider' in df.values:
             emailSub = 'Alert: Reconsider Investment - 15% drop from peak'
             emailBody = df
             notify(emailSub, emailBody)
        elif 'Review' in df.values:
             emailSub = 'Alert: Review Investment - 10% drop from peak'
             emailBody = df
             notify(emailSub, emailBody)
        else:
            pass
    else:
        pass
    return

#set todays date and reference days
today = date.today() 
backdate = today - BDay(4)
backdate = backdate.date()
path = '/home/deepak/finminion'

#loaddata
invested_stocks = pd.read_csv(path + '/invested_stocks.csv', index_col = 0)
sell_trigger = pd.read_csv(path + '/sell_trigger.csv', index_col = 0)


#Get historical data
for index, row in invested_stocks.iterrows() :
    nse_symbol = (row['stocks'])
    # print (nse_symbol)
    sbin = get_history (symbol=nse_symbol, start=backdate, end=today)
    # print(sbin)
    #Check if the new reference is greater, if yes, assign it to 
    if min(sbin.head(3).loc[:,'Close']) > sell_trigger.loc[nse_symbol,'reference']:
        sell_trigger.loc[nse_symbol,'reference'] = min(sbin.head(3).loc[:,'Close'])
           
    #Update close price, and difference
    sell_trigger.loc[nse_symbol,'lastclose'] = sbin.tail(1).ix[0,'Close']
    sell_trigger.loc[nse_symbol,'diff'] = ((sell_trigger.loc[nse_symbol,'lastclose'] - sell_trigger.loc[nse_symbol,'reference'])/ sell_trigger.loc[nse_symbol,'reference'])*100
     
    # check if the last close has dropped more than 20% compared to reference price and update review    
    if sell_trigger.loc[nse_symbol,'lastclose'] < 0.8* sell_trigger.loc[nse_symbol,'reference']:
        sell_trigger.loc[nse_symbol,'review'] = 'Sell'
    elif sell_trigger.loc[nse_symbol,'lastclose'] < 0.85* sell_trigger.loc[nse_symbol,'reference']:
        sell_trigger.loc[nse_symbol,'review'] = 'Reconsider'
    elif sell_trigger.loc[nse_symbol,'lastclose'] < 0.9* sell_trigger.loc[nse_symbol,'reference']:
        sell_trigger.loc[nse_symbol,'review'] = 'Review'
    else:
        sell_trigger.loc[nse_symbol,'review'] = 'False'

#if review is true for any stock, send email
#update sell_trigger file
sell_trigger.to_csv('sell_trigger.csv')

# Call notify review function to check if there is any review worthy stock
notifyReview(sell_trigger)

# print(sell_trigger)



