# send mail function
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import time
from jinja2 import Environment, FileSystemLoader
import configparser

def send_mail(to_, subject_, body_):
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    MYMAIL = config['mail']['user']
    MYPASS = config['mail']['password']
    fromaddr =MYMAIL
    toaddr=to_
    thesub=subject_
    thebody=body_
    thepassword=MYPASS
    domsmtp='smtp.gmail.com'
    smtpport= 587 #needs integer not string

     
    msg = MIMEMultipart('alt text here')
    msg.set_charset('utf8')

     
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = Header(thesub,'utf8')
    _attach = MIMEText(thebody.encode('utf8'),'html','UTF-8')
    msg.attach(_attach)
                       
    server = smtplib.SMTP(domsmtp, smtpport)
    server.starttls()
    server.login(fromaddr, thepassword)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

    server.quit()
    print('mail sent')
    
def todays_date():
    return time.strftime("%d/%m/%Y")

def template(filename_):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template(filename_)
    #output = template.render()
    return template