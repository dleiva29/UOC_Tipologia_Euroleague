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
jugadors_averages=pd.DataFrame()
atributs =[]

url_base="https://www.euroleague.net"
url_web_jugadors_base="https://www.euroleague.net/competition/players?letter="


# Interació per l'abecedari
for letra in abecedari:
    url_web_jugadors=url_web_jugadors_base+letra
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

for i in range(len(links_jugadors)):

    # Web de cada jugador  
    url_jugador_career="https://www.euroleague.net"+links_jugadors.link[i][0]+"#!careerstats"
    page = requests.get(url_jugador_career)
    time.sleep(15)
    soup_jugador = BeautifulSoup(page.content,features="lxml")


    # Extracció atributs (només al primer jugador)
    if not atributs: # si atributs buit
        
        # Atributs averages
        cap  = soup_jugador.find('tr', class_= 'PlayerGridHeader').find_all('th') #només volem 1 taula (hi ha 3 repetides)
        at_prev=""

        for ind in cap:
            at= ind.get_text()
            if at=="%":
                at=at_prev+"_%" #Corregir % sólos
            atributs.append(at)
            at_prev=at
        jugadors_averages=pd.DataFrame(columns=atributs[2:]) 
        
        # Atributs descripció
        atributs_jugador = [value 
           for element in soup_jugador.find('div',class_="summary-first").find_all('span',class_=True)
           for value in element["class"]]

        atributs_jugador.append("position")

        for element in soup_jugador.find('div',class_="summary-second").find_all('span'):
            at=element.get_text().split(": ")[0]
            atributs_jugador.append(at)

        jugadors_desc=pd.DataFrame(columns=atributs_jugador)



    # Extracció averages
    items=soup_jugador.find('tr', class_='PlayerGridRow AverageFooter')
        
    if not items:
        a_series = pd.Series(dtype=pd.StringDtype(), index = jugadors_averages.columns)
    else:
        averages=items.get_text().split()[1:]
        a_series = pd.Series(averages, index = jugadors_averages.columns)
    
    jugadors_averages=jugadors_averages.append(a_series,ignore_index=True)
    
    
    soup_desc=soup_jugador.find('div',class_="summary").find_all(text=True)
    
     # Extracció descripcions
    indices = [2, 5, 7]
    selected_elements = [soup_desc[index] for index in indices]


    for element in soup_jugador.find('div',class_="summary-second").find_all('span'):
        at=element.get_text().split(": ")[1]
        selected_elements.append(at)

    a_series = pd.Series(selected_elements, index = jugadors_desc.columns)
    jugadors_desc=jugadors_desc.append(a_series,ignore_index=True)



# Unió datasets    
jugadors_descAverages=pd.concat([jugadors_desc,jugadors_averages],axis=1) # Unir datasets descripció i averages
jugadors= pd.concat([jugadors,jugadors_descAverages],axis=1) #Unir datasets noms jugadors amb les seves dades


jugadors.to_csv("jugadors.csv",index=False)