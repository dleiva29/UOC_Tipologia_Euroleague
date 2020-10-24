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
    
