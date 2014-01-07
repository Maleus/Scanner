import smtplib
import time
import os
#Method for emailing if a problem arises
def notify():

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    sender = 'SERVER_ALERT@company.com'
    recipient = 'erik.dominguez@mosaik.com'
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
    session.login('mosaik.server.alerts@gmail.com', 'M0saik!!')

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
