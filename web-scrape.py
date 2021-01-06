from bs4 import BeautifulSoup as bs
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


browser = webdriver.Chrome(ChromeDriverManager().install())
urlS=['https://medium.com/search?q=data%20science',
      'https://medium.com/search?q=big%20data',
      'https://medium.com/search?q=deep%20learning']
fields = ['Title', 'body', 'tags']


class GetPostsURLS:
    post_elems = []
    def __init__(self, url:str):
        browser.get(url)
        time.sleep(1)
        elem = browser.find_element_by_tag_name("body")
        no_of_pagedowns = 5000
        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            no_of_pagedowns-=1
            self.PostUrls = self.getPostURLS()
        for item in self.post_elems :
            self.blogPost(item.get_attribute("href"))

    def blogPost(self, link):
        try:
            print(link)
            article = requests.get(link)
            time.sleep(2)
            soup = bs(article.content, 'html.parser')
            article = ''
            tags = []
            try:
                heading = soup.find('h1').text
            except Exception as e:
                print("!111111111111111111111111111111111111111111111111111")
                print(link)
                return
            for para in soup.find_all('p'):
                p = para.text
                p = p.strip('/u')
                article = article + ' ' + p

            classForTag = ['ce cf','ba bb','bu bv','bz ca', 'bg bh', 'bs bt']
            
            for classitem in classForTag :
                mtags = soup.find_all('ul', {'class': classitem})
                if len(mtags) > 0:
                    break

            lis = []
            for li in mtags:
                for data in li.find_all('li'):
                    lis.append(data.text)
            someList = [heading, article, tuple(lis), link]
            df = pd.DataFrame.from_records([{'Title': heading, 'Body': article, "tags" : tuple(lis), "link" : link}])
            df.to_csv("medium.csv", mode='a', header=False);

        except Exception as e:
            raise e


    def getPostURLS(self) -> list:
        self.post_elems = browser.find_elements_by_css_selector("div[class='postArticle-readMore']>a")




for url in urlS:
    parser = GetPostsURLS(url)
