import requests
from bs4 import BeautifulSoup
from newspaper import Article
import pandas as pd
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv 
def repeatitive(links,urls) :
     for link in links :
        if link['href'] in urls :
            return True
     return False  


def scrap_year ():
    page = 1
    scraped_data = []
    url_list = []
    while page < 16  :
        page +=1
        main_page_url = "https://www.varzesh3.com/news?page={page}"
        html = requests.get(main_page_url).text #download html of the page
        soup = BeautifulSoup(html,features='lxml')
        links = soup.find_all('a',class_='title')
        if  repeatitive(links,scraped_data):
            break
        for link in tqdm(links):
            page_url = link['href']
            url_list.append(link['href'])
            try:
                article = Article(page_url)
                article.download()
                article.parse()
                scraped_data.append({'url':page_url,'text':article.text , 'title':article.title})
            except:
                print(f"fail to proccess page: {page_url} ")

    df = pd.DataFrame(scraped_data)
    df.to_csv(f"varzesh3.csv")          

    vectorizer = TfidfVectorizer(lowercase=True)
    vectorizer.fit('varzesh3.csv')
    lines = []
    with open('varzesh3.csv', 'rb') as f:
     reader = csv.reader(f)

    
    
if __name__ == '__main__' :
    scrap_year()