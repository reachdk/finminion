#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 15:19:25 2017

@author: deepak.ppe
"""

# Evaluate whether an alert needs to be sent or not

# Alert levels = P3 ~ -5%, P2 ~ -10%, P1 ~ 15%, P0 ~ Sell
    
import pandas as pd
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


df = pd.read_csv('sell_trigger.csv', index_col = 0)

def notify(mailsub, mailbody):
    fromaddr = "kdeepu@gmail.com"
    toaddr = "netmaildeepak@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
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


def notifyReview(flag, df):
      
    df = df[df.review.str.contains("Reconsider|Review|Sell")]
    df = df.iloc[:,[2,3]]
    df.iloc[:,[0]] = df.iloc[:,[0]].apply(pd.Series.round)
    
    if not df.empty:
         if df.review.str.contains('Sell'):
             emailSub = 'Alert: SELL NOW - 20% drop from peak'
             emailBody = df
             notify(emailSub, emailBody)
         elif df.review.str.contains('Reconsider'):
             emailSub = 'Alert: Reconsider Investment - 15% drop from peak'
             emailBody = df
             notify(emailSub, emailBody)
         elif df.review.str.contains('Review'):
             emailSub = 'Alert: Review Investment - 10% drop from peak'
             emailBody = df
             notify(emailSub, emailBody)
         else:
            pass
    else:
        pass
    