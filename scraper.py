  
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
        #self.abecedari=string.ascii_uppercase #Iterar per tot l'abecedari
        self.abecedari= 'B'
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
    
    def __load_jugadors(self,soup):
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
            
    def __create_atributs(self):
        url_jugador_career=self.url_base+self.links_jugadors.link[0][0]+"#!careerstats"
        soup_jugador= self.__download_html(url_jugador_career)
        headers  = soup_jugador.find('tr', class_= 'PlayerGridHeader').find_all('th')
        
        atribut_prev=""
        for head in headers:
            atribut= head.get_text()
            if atribut=="%":
                atribut=atribut_prev+"_%" #Corregir % sólos
            self.atributs.append(atribut)
            atribut_prev=atribut
        
        self.jugadors_averages=pd.DataFrame(columns=self.atributs[2:]) 
        self.jugadors_temporada = pd.DataFrame(columns=self.atributs)
        self.colnames_jug_temp = self.jugadors_temporada.columns
        
        # Atributs descripció
        atributs_jugador = [value 
           for element in soup_jugador.find('div',class_="summary-first").find_all('span',class_=True)
           for value in element["class"]]

        atributs_jugador.append("position")

        for element in soup_jugador.find('div',class_="summary-second").find_all('span'):
            atribut=element.get_text().split(": ")[0]
            atributs_jugador.append(atribut)

        self.jugadors_desc=pd.DataFrame(columns=atributs_jugador)
        
        
    def __has_date(self,soup_jugador):
        try: 
            eurolliga = soup_jugador.find('span',id= 'ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_ctl01_ctl03_ctl00_lblCompetitionName').get_text() == "Euroleague"
        except: 
            eurolliga = False
        
        self.items=soup_jugador.find('tr', class_='PlayerGridRow AverageFooter')
        
        if eurolliga and self.items:
            return True
        else:
            return False
        
    def __data(self,soup_jugador, index):
        
        if self.__has_date(soup_jugador):
            
            #averages
            averages=self.items.get_text().split()[1:]
            a_series = pd.Series(averages, index = self.jugadors_averages.columns)
        
            #temporada
            stat_temp_tot = soup_jugador.find('div', class_ ='PlayerPhaseStatisticsContainer table-responsive-container')
            element = stat_temp_tot.find('tr', class_="PlayerGridRow")
            for element in stat_temp_tot.find_all('tr', class_="PlayerGridRow"):
                stat_temp = element.get_text().split('\n') #eliminar \n. No es fa split() perque separa nomEquip
                stat_temp = [i for i in stat_temp if i != ""] #eliminar blanks
                
                if not stat_temp[0] in ["Totals", "Averages"]: #nomes guarda les temporada
                    stat_temp_series = pd.Series(stat_temp, index = self.colnames_jug_temp)
                    
                    #afegir nom jugador dataset temporada
                    nom_jug = pd.Series({"name_Complet":self.jugadors['name_Complet'][index]}) #Corregit [] al nom
                    stat_temp_series = pd.concat([nom_jug,stat_temp_series])
                    self.jugadors_temporada=self.jugadors_temporada.append(stat_temp_series,ignore_index=True)
        else:
            a_series = pd.Series(dtype=pd.StringDtype(), index = self.jugadors_averages.columns)
    
        self.jugadors_averages=self.jugadors_averages.append(a_series,ignore_index=True)
        
                
    def scraper(self):
        start_time = time.time()
        for letra in self.abecedari:
            soup=self.__download_html(self.url_web_jugadors_base,letra)
            self.__load_jugadors(soup)
            print('Lletra: ',letra)
                      
            
        if not self.atributs:
            # si atributs buit            
            self.__create_atributs()
                
        #for i in range(len(self.links_jugadors)):
        for i in range(3)   :
            url_jugador_career="https://www.euroleague.net"+self.links_jugadors.link[i][0]+"#!careerstats"
            soup=self.__download_html(url_jugador_career)     
            jug = self.__load_jugadors(soup)
            print('seguent jugador: ', i, self.__has_date(soup))
            self.__data(soup,i)
            
        print('Temporada a temporada:')
        print(self.jugadors_temporada)
        print('Averages:')
        print(self.jugadors_averages)
            
            
            
            
            
    
    
    
    











