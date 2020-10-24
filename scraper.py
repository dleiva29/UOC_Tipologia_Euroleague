  
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
    
    
      
      
      

      
      
      




start_time = time.time()










