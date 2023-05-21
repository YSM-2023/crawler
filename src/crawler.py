import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pymysql
from dotenv import load_dotenv
import os 

class Crawler:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_argument('--headless') #내부 창을 띄울 수 없으므로 설정
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )
        self.driver.get('https://www.makeup-in.com/losangeles/exhibitors/')
    def crawl(self):
        cookieBtn = self.driver.find_element(By .XPATH, '//*[@id="didomi-notice-agree-button"]').click()

        gridBox = self.driver.find_element(By .XPATH, '//*[@id="content"]/div/div[1]/section[6]/div/div/div/div[3]/div/div/div')
        gridElements = gridBox.find_elements(By .CLASS_NAME, 'ex_name')
        exhibitors_li = []
        for gridElement in gridElements:
            exhibitors_li.append(gridElement.text)
        print(len(exhibitors_li))
        self.driver.quit()
        return exhibitors_li

class DB:
    def __init__(self) -> None:
        load_dotenv()
        user = os.environ.get('DbUser')
        pwd = os.environ.get('DbPwd')
        self.connect = pymysql.connect(host='127.0.0.1', user=user, password=pwd, db='crawleddata', charset='utf8mb4')
        self.cursor = self.connect.cursor()
    def insert(self, datas):
        for name in datas:
            query = """INSERT INTO company (name) VALUES(%s);"""
            param = (name, )
            self.cursor.execute(query, param)
            self.connect.commit()
        self.connect.close()

crawler = Crawler()
exhibitors = crawler.crawl()
db = DB()
db.insert(exhibitors)
