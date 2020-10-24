  
## Creación de la clase scraper. Mediante web scraping extrae las estadísticas de los jugadores de la Euroleague de la web 'www.euroleague.net'.
## Genera dos ficheros .csv, uno con las estadísiticas medias en la Euroleague y otro con las estadísticas desglosadas por temporada. 


import os
import pandas as pd
import requests
import time 
import string
from bs4 import BeautifulSoup

class EuroleagueScraper():
    
    def __init__(self):
        self.abecedari=string.ascii_uppercase #Iterar per tot l'abecedari
        self.links_jugadors=pd.DataFrame()
        self.jugadors_averages=pd.DataFrame()
        self.jugadors=pd.DataFrame()
        self.atributs =[]
        self.url_base="https://www.euroleague.net"
        self.url_web_jugadors_base="https://www.euroleague.net/competition/players?letter="
        
    def __download_html(self, url, letra=""):
        time.sleep(15)
        url_compuesta=url+letra
        page = requests.get(url_compuesta)
        soup = BeautifulSoup(page.content,features="lxml")
        return soup
    
    def __get_jugadors(self,soup):
        items=soup.find_all('div', class_='item')
        for link in items:
            l=[link.a.get('href')]
            name_complet=[link.a.get_text().strip()][0]
            self.links_jugadors=self.links_jugadors.append({"link":l},ignore_index=True)
            cognom=name_complet.split(", ")[0]
            nom=name_complet.split(", ")[1]
            self.jugadors=self.jugadors.append({"name_Complet":name_complet, 
                                                "cognom":cognom, 
                                                "nom":nom },ignore_index=True)
            self.jugadors=self.jugadors[["name_Complet","cognom","nom"]]
            
        def __get_atributs(self):
            url_jugador_career="https://www.euroleague.net"+self.links_jugadors.link[0][0]+"#!careerstats"
            soup_jugador= self.__download_html()
            cap  = soup_jugador.find('tr', class_= 'PlayerGridHeader').find_all('th')
            at_prev=""

        for ind in cap:
            at= ind.get_text()
            if at=="%":
                at=at_prev+"_%" #Corregir % sólos
            atributs.append(at)
            at_prev=at
        jugadors_averages=pd.DataFrame(columns=atributs[2:]) 
        jugadors_temporada = pd.DataFrame(columns=atributs)
        colnames_jug_temp = jugadors_temporada.columns
        
        # Atributs descripció
        atributs_jugador = [value 
           for element in soup_jugador.find('div',class_="summary-first").find_all('span',class_=True)
           for value in element["class"]]

        atributs_jugador.append("position")

        for element in soup_jugador.find('div',class_="summary-second").find_all('span'):
            at=element.get_text().split(": ")[0]
            atributs_jugador.append(at)

        jugadors_desc=pd.DataFrame(columns=atributs_jugador)
            
            

      

    def scraper(self):
        start_time = time.time()
        for letra in self.abecedari:
            soup=self.__download_html(self.url_web_jugadors_base,letra)
            self.__get_jugadors(soup)
            
    
    
    
    











