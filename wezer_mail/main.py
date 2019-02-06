from bs4 import BeautifulSoup

import requests

from utils import send_mail, todays_date

def decide_headline(headline_):
    headline = ''
    if 'showers' in headline_:
        headline = 'take umbrella'
    elif 'cloudy' in headline_:
        headline = 'some light protection needed'
    else:
        headline = 'nothing to worry about today'
    return '{} - {}'.format(todays_date(), headline.title())

prediction_url = "http://metservice.intnet.mu/index.php"
r  = requests.get(prediction_url)

data = r.text

soup = BeautifulSoup(data, features="html.parser")

fconds = []
cdates = []
fdays = []
for e in soup.findAll("p", {"class": "fcondition"}):
    fconds.append(e.text)
    
for e in soup.findAll("p", {"class": "fday"}):
    fdays.append(e.text)
    
for e in soup.findAll("span", {"class": "cdate"}):
    cdates.append(e.text)
    
news = soup.find("div", {"class": "warning"}).findChildren()
news = [n.text for n in news]
    
data = list(zip(fconds,fdays+cdates))

#for i, d in enumerate(data):
    #print(i, d)
    
#print('[x]', len(fconds), len(cdates), len(fdays))
info = {'general':data[0][0],
        'portlouis':data[7][0],
        'headline':news[0]}

headline = decide_headline(info['portlouis'])
with open('subs.txt', 'r') as f:
    for mail in f:
        send_mail(mail, headline, info['headline'])
