# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 19:32:13 2020

@author: Alvaro and David
"""

import os
import pandas as pd
import requests
import time
import string
from bs4 import BeautifulSoup

abecedari=string.ascii_uppercase
url_web_jugadors_base="https://www.euroleague.net/competition/players?letter="

url_web_jugadors=url_web_jugadors_base+"A"

#page = requests.get(url_web_jugadors)
soup = BeautifulSoup(page.content,features="lxml")


items=soup.find_all('div', class_='item')


links_jugadors=pd.DataFrame()



for link in items:
    l=[link.a.get('href')]
    name=[link.a.get_text().strip()]
    links_jugadors=links_jugadors.append({"link":l,"name":name},ignore_index=True)
   
    
url_jugador_career="https://www.euroleague.net"+links_jugadors.link[0][0]+"#!careerstats"

page = requests.get(url_jugador_career)
soup_jugador = BeautifulSoup(page.content,features="lxml")

print(soup_jugador)