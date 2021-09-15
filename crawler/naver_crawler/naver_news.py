from selenium import webdriver
from multiprocessing import Pool
import pandas as pd


def find_last_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    driver.get(url + '&page=10000')
    result = driver.find_element_by_xpath('//*[@id="main_content"]/div[3]/strong')
    return result.text


def crawling_news(url):
    res = {'title': []}
    driver = webdriver.Chrome('./chromedriver.exe')
    pages = int(find_last_page(url))
    for i in range(pages):
        print(f'{i+1}/{pages}')
        driver.get(url + f'&page={i+1}')
        results = driver.find_elements_by_xpath('//*[@id="main_content"]/div/ul/li/dl/dt/a[@class="nclicks(fls.list)"]')
        for result in results:
            if result.text == '동영상기사': continue
            res['title'].append(result.text)
    return res

if __name__ == '__main__':
    urls = ['https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1='+str(i) for i in range(100, 106)]
    pool = Pool(processes=4)
    pool.map(crawling_news, urls)
