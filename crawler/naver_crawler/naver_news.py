from selenium import webdriver
from multiprocessing import Pool


def find_last_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    driver.get(url + '&page=10000')
    result = driver.find_element_by_xpath('//*[@id="main_content"]/div[3]/strong')
    return result.text


def crawling_news(path):
    date = '20210915'
    menu = {
        '100': '정치', '101': '경제', '102': '사회', '103': '생활/문화', '104': '세계', '105': 'IT/과학'
    }

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)

    url = f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&date={date}&sid1=' + path
    pages = int(find_last_page(url))
    for i in range(pages):
        print(f'{i+1}/{pages}')
        driver.get(url + f'&page={i+1}')
        results = driver.find_elements_by_xpath('//*[@id="main_content"]/div/ul/li/dl/dt/a[@class="nclicks(fls.list)"]')
        for result in results:
            if (result.text == '동영상기사') or (result.text == ''):
                continue
            # print(f'{menu[path]}: {result.text}')
    driver.close()


if __name__ == '__main__':
    urls = [str(i) for i in range(100, 106)]
    pool = Pool(processes=8)
    pool.map(crawling_news, urls)

