import time
from selenium import webdriver
import pandas as pd


data = {'date': [], 'col': [], 'title': [], 'company': []}

url = 'https://sports.news.naver.com/index'
driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)
iter_times = 100

for idx in range(8):
    menu = driver.find_element_by_xpath(f'//ul/li[{idx+2}]/a[@class="link_main_menu"]')
    col = menu.text
    menu.click()
    time.sleep(1)
    sub_menu = driver.find_element_by_xpath(f'//li[{idx + 2}]/ul/li[1]/a')
    sub_menu.click()
    time.sleep(1)
    for i in range(iter_times):
        try:
            contents = driver.find_elements_by_xpath('//li/div/a[@class="title"]')
            comps = driver.find_elements_by_xpath('//li/div/div/span[@class="press"]')
            for content, comp in zip(contents, comps):
                data['col'].append(col)
                data['title'].append(content.text)
                data['date'].append(f'{time.strftime("%m")}-{time.strftime("%d")}')
                data['company'].append(comp.text)
            but = driver.find_element_by_xpath(f'//div[@id="_pageList"]/a[@data-id="{i + 2}"]')
            but.click()
            time.sleep(1)
        except:
            try:
                but = driver.find_element_by_xpath(f'//div[@id="_pageList"]/a[@data-id="{i-8}"]')
                but.click()
                but = driver.find_element_by_xpath(f'//div[@id="_pageList"]/a[@class="next"]')
                but.click()
                time.sleep(1)
            except:
                time.sleep(.5)
                break


driver.close()

result = pd.DataFrame(data)
result.to_csv('naver_sports_news.csv', encoding='utf-8-sig')
print(result.shape)
