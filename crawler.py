from bs4 import BeautifulSoup
import requests
import json
import pandas as pd


def get_links(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html5lib")

    #finding paging page
    news_links = soup.find_all("li", {'class':'p1520 art-list pos_rel'})
    
    return news_links

def crawling(links):
    result = []
    for idx, news in enumerate(links):
        news_dict = {}
        news_title = news.find('a',{'class':'f20 ln24 fbo txt-oev-2'}).text
        news_url = news.find('a',{'class':'f20 ln24 fbo txt-oev-2'}).get('href')
    
        req_news = requests.get(news_url)
        soup_news = BeautifulSoup(req_news.text,'html5lib')
    
    
        content_news = soup_news.find('div',{'class':'side-article txt-article'})
    
        p = content_news.find_all('p')
        content = ' '.join(item .text for item in p)
        content = content.encode('utf-8','replace')
        
        news_dict['id'] = idx
        news_dict['url'] = news_url
        news_dict['title'] = news_title
        news_dict['content'] = content

        result.append(news_dict)
    
    return result

if __name__== "__main__":
	categories = ['bisnis','sport','lifestyle']
	for cat in categories:
		url = 'https://www.tribunnews.com/'+cat
		links = get_links(url)
    
		contents = crawling(links)
		print('trying to export')
		df = pd.DataFrame(contents)
		df.to_csv(cat+'.csv')
		print(df.shape)