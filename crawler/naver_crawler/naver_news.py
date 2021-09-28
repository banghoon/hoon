from selenium import webdriver
from multiprocessing import Pool
import numpy as np
import pandas as pd
from selenium.webdriver.common.keys import Keys


def find_last_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    driver.get(url + '&page=10000')
    result = driver.find_element_by_xpath('//*[@id="main_content"]/div[3]/strong')
    last_page = result.text
    driver.close()
    return last_page


# def get_news_text(url):
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')
#     options.add_argument('window-size=1920x1080')
#     options.add_argument("disable-gpu")
#
#     driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
#     driver.get(url)
#     try:
#         url_res = driver.find_element_by_xpath('//div[@id="articleBodyContents"]')
#         res = [url_res.text.replace('\n', '')]
#     except:
#         try:
#             url_res = driver.find_element_by_xpath('//div[@id="newsEndContents"]')
#             res = [url_res.text.replace('\n', '')]
#         except:
#             res = [np.nan]
#     driver.close()
#     return res


def crawling_news(path):
    dates = [f'2021092{i}' for i in range(2, 8)]  # add date if you want

    menu = {
        '100': '정치', '101': '경제', '102': '사회', '103': '생활/문화', '104': '세계', '105': 'IT/과학'
    }
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--mute-audio")

    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)

    for date in dates:
        url = f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&date={date}&sid1=' + str(path)
        pages = int(find_last_page(url))
        datalist = []

        for page in range(pages):
            print(f'-------------------{page+1}/{pages}-------------------')
            driver.get(url + f'&page={page+1}')

            for i in [1, 2]:
                results = driver.find_elements_by_xpath(
                    f'//div[@id="main_content"]/div/ul[{i}]/li/dl/dt/a[@class="nclicks(fls.list)"]')
                comps = driver.find_elements_by_xpath('//div[@id="main_content"]/div/ul/li/dl/dd/span[2]')

                for comp, result in zip(comps, results):
                    if (result.text == '동영상기사') or (result.text == ''):
                        continue
                    result.send_keys(Keys.CONTROL + "\n")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.implicitly_wait(20)
                    try:
                        url_res = driver.find_element_by_xpath('//div[@id="articleBodyContents"]')
                        res = url_res.text.replace('\n', '')

                    except:
                        try:
                            url_res = driver.find_element_by_xpath('//div[@id="newsEndContents"]')
                            res = url_res.text.replace('\n', '')

                        except:
                            res = np.nan

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    driver.implicitly_wait(20)

                    datalist.append({
                        'date': date,
                        'category': menu[path],
                        'title': result.text,
                        'company': comp.text,
                        'url': result.get_attribute("href"),
                        'text': res
                    })

        pd.DataFrame(datalist).to_csv(f'./data/news_{date}_{path}.csv', encoding='utf8')
        print(f'{date}_{path}_END-------------------')

    driver.quit()


def to_sqlite3(cursor):
    pass


if __name__ == '__main__':
    # urls = ['105']
    urls = [str(i) for i in range(100, 106)]
    with Pool(processes=8) as pool:
        final = pool.map(crawling_news, urls)

