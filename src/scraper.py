import os
import pandas as pd
import requests
import time 
import string
from bs4 import BeautifulSoup

class EuroleagueScraper():
    
    def __init__(self):
        self.alphabet=string.ascii_uppercase
        self.links_players=pd.DataFrame()
        self.players=pd.DataFrame()
        self.attribute =[]
        self.url_base="https://www.euroleague.net"
        self.url_web_players_base="https://www.euroleague.net/competition/players?letter="
        
        
    def __download_html(self, url, l=""):
        time.sleep(15) #Crawl-delay robots.txt
        url_long=url+l
        page = requests.get(url_long)
        soup = BeautifulSoup(page.content,features="lxml")
        return soup
    
    
    def __load_players(self,soup):
        items=soup.find_all('div', class_='item')
        for link in items:
            l=[link.a.get('href')]
            full_name=[link.a.get_text().strip()][0]
            self.links_players=self.links_players.append({"link":l},ignore_index=True)
            surname=full_name.split(", ")[0]
            name=full_name.split(", ")[1]
            self.players=self.players.append({"full_name":full_name, 
                                                "surname":surname, 
                                                "name":name },ignore_index=True)
            self.players=self.players[["full_name","surname","name"]]
            
            
    def __create_attribute(self):
        # Use first player for extracting colnames and attributes
        url_player_career=self.url_base+self.links_players.link[0][0]+"#!careerstats"
        soup_player= self.__download_html(url_player_career)
        
        # stats colnames
        headers  = soup_player.find('tr', class_= 'PlayerGridHeader').find_all('th')
        prev_att=""
        for h in headers:
            att= h.get_text()
            if att=="%":
                att=prev_att+"_%" 
            self.attribute.append(att)
            prev_att=att
        
        #create datasets 
        self.euroleaguePlayers_average=pd.DataFrame(columns=self.attribute[2:]) 
        self.euroleaguePlayers_season = pd.DataFrame(columns=self.attribute)
        self.colnames_temp = self.euroleaguePlayers_season.columns
        
        # player attributes
        attribute_player = [value.capitalize() 
           for element in soup_player.find('div',class_="summary-first").find_all('span',class_=True)
           for value in element["class"]]

        attribute_player.append("Position")

        for element in soup_player.find('div',class_="summary-second").find_all('span'):
            att=element.get_text().split(": ")[0]
            attribute_player.append(att)

        self.data_desc=pd.DataFrame(columns=attribute_player)
        
        
    def __has_date(self,soup_player):
        # check if there are data and they are from Euroleague
        try: 
            dataEuroleague = soup_player.find('span',id= 'ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_ctl01_ctl03_ctl00_lblCompetitionName').get_text() == "Euroleague"
        except: 
            dataEuroleague = False
        
        data_player=soup_player.find('tr', class_='PlayerGridRow AverageFooter')
        
        if dataEuroleague and data_player:
            return True
        else:
            return False
        
        
    def __data(self,soup_player, index):
        
        if self.__has_date(soup_player):
            
            #average data
            averages=soup_player.find('tr', class_='PlayerGridRow AverageFooter').get_text().split()[1:]
            stat_ave_series = pd.Series(averages, index = self.euroleaguePlayers_average.columns)
        
            #season data
            stat_temp_tot = soup_player.find('div', class_ ='PlayerPhaseStatisticsContainer table-responsive-container')
            element = stat_temp_tot.find('tr', class_="PlayerGridRow")
            for element in stat_temp_tot.find_all('tr', class_="PlayerGridRow"):
                stat_temp = element.get_text().split('\n') 
                stat_temp = [i for i in stat_temp if i != ""] 
                
                if not stat_temp[0] in ["Totals", "Averages"]:
                    stat_temp_series = pd.Series(stat_temp, index = self.colnames_temp)
                    
                    # add name to season data
                    player_name = pd.Series({"full_name":self.players['full_name'][index]}) 
                    stat_temp_series = pd.concat([player_name,stat_temp_series])
                    
                    self.euroleaguePlayers_season=self.euroleaguePlayers_season.append(stat_temp_series,ignore_index=True)
        else:
            stat_ave_series = pd.Series(dtype=pd.StringDtype(), index = self.euroleaguePlayers_average.columns)
    
        self.euroleaguePlayers_average = self.euroleaguePlayers_average.append(stat_ave_series,ignore_index=True)
        
        # attributes data
        soup_desc=soup_player.find('div',class_="summary").find_all(text=True)
        desc = [soup_desc[ind] for ind in [2, 5, 7]]
        for element in soup_player.find('div',class_="summary-second").find_all('span'):
            at=element.get_text().split(": ")[1]
            desc.append(at)

        desc_series = pd.Series(desc, index = self.data_desc.columns)
        self.data_desc=self.data_desc.append(desc_series,ignore_index=True)
    
    
    def scraper(self):
        start_time = time.time()
        
        #Extract url links
        for i in self.alphabet:
            soup=self.__download_html(self.url_web_players_base,i)
            self.__load_players(soup)
                      
        #Extract colnames for every data
        if not self.attribute:  
            self.__create_attribute()
                
        #Extract data for all players
        for i in range(len(self.links_players)):
            url_player_career="https://www.euroleague.net"+self.links_players.link[i][0]+"#!careerstats"
            soup=self.__download_html(url_player_career)     
            self.__data(soup,i)
            
        # Join data_average with descriptors and players
        data_player_average_desc=pd.concat([self.data_desc,self.euroleaguePlayers_average],axis=1) 
        self.euroleaguePlayers_average= pd.concat([self.players,data_player_average_desc],axis=1)
        
        
        #time elapsed
        end_time = time.time()
        print ("\nelapsed time': " + str(round(((end_time - start_time) / 60) , 2)) + " minutes" )  
        
         
    def data2csv(self):
        # save datasets
        # create or overwrite previous csv
        self.euroleaguePlayers_season.to_csv("csv/euroleaguePlayers_season.csv",index=False)
        self.euroleaguePlayers_average.to_csv("csv/euroleaguePlayers_average.csv",index=False)
        