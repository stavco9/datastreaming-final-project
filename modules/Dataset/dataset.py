import bs4
import requests
import pandas as pd
from random import shuffle

class Dataset:
    def __init__(self, links_base_url, links_uri, links_column):
        self.links_base_url = links_base_url
        self.links_uri = links_uri
        self.links_column = links_column
        self.articles_list = self.build_articles_list_from_table()

    def build_articles_list_from_table(self):
        response = requests.get(f"{self.links_base_url.rstrip('/')}/{self.links_uri}",headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs4.BeautifulSoup(response.text,'html.parser')
        table = soup.find('table')
        data = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 0:
                cols = row.find_all('th')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])  # Get rid of empty values
        
        headers = data.pop(0)
        df = pd.DataFrame(data, columns=headers)
        articles_list = list(df.loc[:,self.links_column])
        shuffle(articles_list)
        return articles_list
    
    def build_words_list(self, num_of_articles):
        shuffle(self.articles_list)

        words_list = {}

        for article in self.articles_list[0:min(num_of_articles, len(self.articles_list))]:
            response = requests.get(f"{self.links_base_url.rstrip('/')}/{article}",headers={'User-Agent': 'Mozilla/5.0'})
            soup = bs4.BeautifulSoup(response.text,'html.parser')
            
            articale_list = soup.body.get_text(' ', strip=True).split()
            shuffle(articale_list)
            words_list[article] = articale_list
        
        return words_list