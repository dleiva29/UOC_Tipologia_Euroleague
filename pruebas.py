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
atributs =[]

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


# Extracció atributs (només al primer jugador)
if not atributs: # si atributs buit
    cap  = soup_jugador.find('tr', class_= 'PlayerGridHeader').find_all('th') #només volem 1 taula (hi ha 3 repetides)
    at_prev=""

    for ind in cap:
        at= ind.get_text()
        if at=="%":
            at=at_prev+"_%" #Corregir % sólos
        atributs.append(at)
        at_prev=at
    jugadors_averages=pd.DataFrame(columns=atributs[2:]) 


# Extracció averages
items=soup_jugador.find('tr', class_='PlayerGridRow AverageFooter')
averages=items.get_text().split()[1:]

a_series = pd.Series(averages, index = jugadors_averages.columns)
jugadors_averages=jugadors_averages.append(a_series,ignore_index=True)



# Unir dataframe jugadors amb dataframe jugadors_averges
# desprès de l'extracció dels averages de tots els jugadors

#jugadors_averages=pd.concat([jugadors,jugadors_averages], axis=1)  

<<<<<<< HEAD
#print(jugadors_averages)
=======
print(jugadors_averages)

##Alvaro
#Exemple estadístiques per a 
# https://www.euroleague.net/competition/players/showplayer?pcode=003733&seasoncode=E2020#!careerstats
#Extracció de la capçalera de les estadistiques
atributs =[]
cap  = soup_jugador.find('tr', class_= 'PlayerGridHeader').find_all('th') #només volem 1 taula (hi ha 3 repetides)
for ind in cap:
    atributs.append(ind.get_text())

print(atributs)


#Extracció average stats 1a caixa - Eurolliga
nom = 'Abalde' #faltaria fer l'scrapping del nom del jugador
avg_stat = []
stats_jugador=soup_jugador.find('tr', class_ ='PlayerGridRow AverageFooter').find_all('td')
for val in stats_jugador:
    avg_stat.append(val.get_text())
    
print(avg_stat)
avg_stat = np.ravel(avg_stat)  #no estic segur si es fa així. Vull convertir uana llista en un vector

# guardar-ho en un dataframe
stats_totals=pd.DataFrame(data= avg_stat, index = atributs)
stats_totals.columns=  [nom]
print(stats_totals.transpose())

#hi ha ua millor manera de fer els dataframes, estic molt rovellat.

# to do: 
# - iterar per a cada jugador de la taula links_jugadors
# - scrapping nom jugador (potser no cal)
>>>>>>> 633e3d365248eea6f0571c7cd6a20f0f1bc93b39

