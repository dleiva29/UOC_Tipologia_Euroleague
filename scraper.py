  
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
        self.abecedari= 'A'
        self.links_jugadors=pd.DataFrame()
        #self.data_average=pd.DataFrame()
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
        
        self.data_average=pd.DataFrame(columns=self.atributs[2:]) 
        self.data_temporada = pd.DataFrame(columns=self.atributs)
        self.colnames_jug_temp = self.data_temporada.columns
        
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
        
        items=soup_jugador.find('tr', class_='PlayerGridRow AverageFooter')
        
        if eurolliga and items:
            return True
        else:
            return False
        
    def __data(self,soup_jugador, index):
        
        if self.__has_date(soup_jugador):
            
            #averages
            averages=soup_jugador.find('tr', class_='PlayerGridRow AverageFooter').get_text().split()[1:]
            a_series = pd.Series(averages, index = self.data_average.columns)
        
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
                    self.data_temporada=self.data_temporada.append(stat_temp_series,ignore_index=True)
        else:
            a_series = pd.Series(dtype=pd.StringDtype(), index = self.data_average.columns)
    
        self.data_average = self.data_average.append(a_series,ignore_index=True)
        
        #Descriptors
        soup_desc=soup_jugador.find('div',class_="summary").find_all(text=True)
      
        descriptor = [soup_desc[ind] for ind in [2, 5, 7]]

        for element in soup_jugador.find('div',class_="summary-second").find_all('span'):
            at=element.get_text().split(": ")[1]
            descriptor.append(at)

        a_series = pd.Series(descriptor, index = self.jugadors_desc.columns)
        self.jugadors_desc=self.jugadors_desc.append(a_series,ignore_index=True)
    

        # Unió datasets    
        dataJug_average_desc=pd.concat([self.jugadors_desc,self.data_average],axis=1) # Unir datasets descripció i averages
        self.jugadors= pd.concat([self.jugadors,dataJug_average_desc],axis=1) #Unir datasets noms jugadors amb les seves dades
        
                
    def scraper(self):
        start_time = time.time()
        for letra in self.abecedari:
            soup=self.__download_html(self.url_web_jugadors_base,letra)
            self.__load_jugadors(soup)
                      
        if not self.atributs:
            # si atributs buit            
            self.__create_atributs()
                
        #for i in range(len(self.links_jugadors)):
        for i in range(1):
            url_jugador_career="https://www.euroleague.net"+self.links_jugadors.link[i][0]+"#!careerstats"
            soup=self.__download_html(url_jugador_career)     
            jug = self.__load_jugadors(soup)
            self.__data(soup,i)
            
        print('Temporada a temporada:')
        print(self.data_temporada)
        print('Averages:')
        print(self.jugadors)
        
        
    def data2csv(self):
        self.data_temporada.to_csv("csv/data_temporada.csv",index=False)
        self.jugadors.to_csv("csv/data_averages.csv",index=False)
        
        #        #Temporada a temporada
        # file = open("csv/data_temporada.csv", "w+")

        # for i in range(len(self.data_temporada)):
        #     for j in range(len(self.data_temporada[i])):
        #         file.write(self.data_temporada[i][j] + ";")
        #     file.write("\n");
            
        # #Temporada a temporada
        # file2 = open("csv/data_averages.csv", "w+")

        # for i in range(len(self.jugadors)):
        #     for j in range(len(self.jugadors[i])):
        #         file2.write(self.jugadors[i][j] + ";")
        #     file2.write("\n");
            
            
            
            
            
    
    
    
    











