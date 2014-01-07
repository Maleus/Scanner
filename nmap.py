# This is a simple script that will perform an Nmap ping scan, compare it to a preconfigured list, and notify you if there are any changes between the baseline list and the new scan.
# 
# You must have ip_list.txt configured with a list of IP addresses for the Nmap scan in the same directory.
# 
# You must have a baseline.txt file configured with the expected output of the # scan in the same directory.
# The output will be listed in a text file named by the date on the computer.

#!/bin/python
import smtplib
import time
import os
#Method for emailing if a problem arises
def notify():

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    sender = 'SERVER_ALERT@company.com'
    recipient = 'YOUR EMAIL ADDRESS HERE'# Must enter the receiving email address
    subject = 'SERVER STATUS ALERT'
    body = str(problems) + " Status has changed"

    body = "" + body + ""

    headers = ["From: " + sender,
       "Subject: " + subject, 
       "To: " + recipient, 
       "MIME-Version: 1.0",
       "Content-Type: text/html"]
    headers = "\r\n".join(headers)

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.login('EMAIL HERE', 'EMAIL PASSWORD HERE')#Must enter a valid gmail account address and password

    session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
    session.quit()

#Scanning with nmap and naming the scan the date
timestr = time.strftime("%m-%d-%y")

daily_scan = open(timestr+".txt", 'w')

os.system("nmap -sn -iL ip_list.txt -oG scan.txt -T2")

scan_data = open("scan.txt", 'r').readlines()

#Checking for changes
for line in scan_data:
    if "Host:" in line:
        daily_scan.write(str(line))

daily_scan.close()

os.system('rm scan.txt')

baseline = open('baseline.txt', 'r').readlines()

daily_check = open(timestr+".txt", 'r').readlines()

problems = [line for line in baseline if line not in daily_check]
if problems:
    notify()
else:
    print "no problem"
