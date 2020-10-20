# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 19:32:13 2020

@author: Alvaro and David
"""

import os
import pandas as pd
import requests
import time # Per afegir sleep(15) entre petició
import string
from bs4 import BeautifulSoup

abecedari=string.ascii_uppercase #Iterar per tot l'abecedari
links_jugadors=pd.DataFrame()
jugadors=pd.DataFrame()
jugadors_averages=pd.DataFrame(columns=("G",
                                        "Pts",
                                        "Avg",
                                        "2FG",
                                        "2FG_%",
                                        "3FG",
                                        "3FG_%",
                                        "FT",
                                        "FT_%",
                                        "Reb",
                                        "St",
                                        "As",
                                        "Bl")) # Es podria extreure automàticament els noms
url_base="https://www.euroleague.net"
url_web_jugadors_base="https://www.euroleague.net/competition/players?letter="


# Interació per l'abecedari
url_web_jugadors=url_web_jugadors_base+"A"

page = requests.get(url_web_jugadors)

time.sleep(15)

soup = BeautifulSoup(page.content,features="lxml")
items=soup.find_all('div', class_='item')




for link in items:
    l=[link.a.get('href')]
    name_complet=[link.a.get_text().strip()][0]
    links_jugadors=links_jugadors.append({"link":l},ignore_index=True)
    cognom=name_complet.split(", ")[0]
    nom=name_complet.split(", ")[1]
    jugadors=jugadors.append({"name_Complet":name_complet, "cognom":cognom, "nom":nom },ignore_index=True)
    

# Web de cada jugador  
url_jugador_career="https://www.euroleague.net"+links_jugadors.link[0][0]+"#!careerstats"

page = requests.get(url_jugador_career)
soup_jugador = BeautifulSoup(page.content,features="lxml")


# Extracció averages
items=soup_jugador.find('tr', class_='PlayerGridRow AverageFooter')
averages=items.get_text().split()[1:]

a_series = pd.Series(averages, index = jugadors_averages.columns)
jugadors_averages=jugadors_averages.append(a_series,ignore_index=True)


print(jugadors_averages)