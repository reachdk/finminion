inca's #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 10:30:14 2017

@author: deepak.ppe
"""
import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
 
fromaddr = "kdeepu@gmail.com"
toaddr = "netmaildeepak@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Notification from "
 
body = str(sell_trigger)
msg.attach(MIMEText(body, 'plain'))



server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "vW4AJPu7u1wk")
text = msg.as_string()
msg = "Notification mail via Python"
server.sendmail(fromaddr, toaddr, text)
server.quit()
