import requests
from bs4 import BeautifulSoup 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pymysql
from dotenv import load_dotenv
import os 
from ast import literal_eval


# # 1번 사이트
# webpage=requests.get('https://www.medisvc.com/cosmetics/fo/cosmeticscompanylist.sd')
# # print(webpage)

# soup=BeautifulSoup(webpage.content, "html.parser")
# names=soup.find_all("a", attrs={'class':'text-theme-colored'})
# names=soup.find_all("a", attrs={'class':'text-theme-colored'})
# # ex_list=soup.find_all("ul", attrs={'class':'elementor-nav-menu'})

# table = soup.find("table", attrs={"class":"table table-striped table-hover table-bordered"})
# tbody = table.select_one('tbody')
# trs = tbody.select('tr')

# f = open("medisvc.txt", 'w', encoding='utf-8')

# for tr in trs:
#     name = tr.select('td')[0].text.strip()
#     address = tr.select('td')[1].text.strip()
#     type = tr.select('td')[2].text.strip()
#     owner = tr.select('td')[3].text.strip()
 
#     print('업체명: {0}, 주소: {1}, 업종: {2}, 대표자명: {3}'.format(name, address, type, owner))
#     f.write(name+"|"+address+"|"+type+"|"+owner+"\n")
    
# f.close()

# import requests
# from bs4 import BeautifulSoup 
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# ## Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
# driver = webdriver.Chrome('/Users/user/Downloads/chromedriver')

# #3번 사이트
# headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
# webpage=requests.get('https://bronnerbros.com/exhibitor-list/', headers=headers)

# soup=BeautifulSoup(webpage.content, "html.parser")
# frame = soup.find('iframe', attrs={"class":"iframe-class"})

# res1 = requests.get(frame['src'])
# frame_soup = BeautifulSoup(res1.content, 'html.parser')
# frame2 = frame_soup.find('frame')

# res2 = requests.get(frame2['src'])
# frame_soup2 = BeautifulSoup(res2.content, 'html.parser')

# # # BeautifulSoup으로 기업명 저장
# # exhibitor_list = frame_soup2.find_all('a', attrs={"class":"ex"})
# f = open("bronnerbros.txt", 'w', encoding='utf-8')
# # for item in exhibitor_list:
# #     f.write(item.text.strip()+"\n")

# # selenuim으로 기업명 저장 및 기업명 클릭 후 상세 설명 저장
# driver.get(frame2['src'])
# sample = driver.find_elements(By.CLASS_NAME, "ex")
# for item in sample:
#     f.write(item.text.strip()+"|") # 기업명 저장
#     item.send_keys('\n') # 클릭
#     time.sleep(2)
#     desc = driver.find_element(By.XPATH, '//*[@id="profileTab"]/div')
#     f.write(desc.text.replace("\n"," ")+"\n") # 기업 상세 설명 저장

# f.close()


# import pymysql
# from dotenv import load_dotenv
# import os

# load_dotenv()

# conn = pymysql.connect(host=os.environ.get('DB_HOST'),
#                         user=os.environ.get('DB_USER'),
#                         password=os.environ.get('DB_PASSWORD'),
#                         db=os.environ.get('DB_NAME'),
#                         charset='utf8')

# cur = conn.cursor()

# #table 생성
# cur.execute("create table company( id INT NOT NULL AUTO_INCREMENT, name VARCHAR(60) NOT NULL, address VARCHAR(100), type VARCHAR(50), owner VARCHAR(50), contact VARCHAR(30), website VARCHAR(50), item VARCHAR(50), description VARCHAR(4000), PRIMARY KEY(id));")

# # medisvc 데이터 저장
# f1 = open("medisvc.txt", 'r', encoding='utf-8')
# lines = f1.readlines()   
# for line in lines:   
#     data=line.split('|')
#     name=data[0].strip()
#     address=data[1].strip()
#     type=data[2].strip()
#     owner=data[3].strip()
#     cur.execute("INSERT INTO company (name, address, type, owner) VALUES(%s, %s, %s, %s)", (name, address, type, owner))

# f1.close()


# # bronnerbros 데이터 저장
# f2 = open("bronnerbros.txt", 'r', encoding='utf-8')
# lines = f2.readlines()   
# for line in lines:   
#     data=line.split('|')
#     name=data[0].strip()
#     description=data[1].strip()
#     cur.execute("INSERT INTO company (name, description) VALUES(%s, %s)", (name, description))

# f2.close()

# conn.commit()
# conn.close()


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
        print("setted webdriver\n")

    def get_request(self, url, headers=""):
        self.driver.get(url)
        if headers=="":
            self.webpage = requests.get(url)
        else:
            self.webpage = requests.get(url, headers=literal_eval(headers))
        soup = BeautifulSoup(self.webpage.content, "html.parser")
        print("got request from website\n")
        return soup

    def set_txt(self, id, table_name, cols):
        f_name = str(id)+".txt"
        f = open(f_name, 'w', encoding='utf-8')
        f.write(table_name+"\n")
        for col in cols:
            f.write(col)
            if not col is cols[-1]:
                f.write("|")
        f.write("\n")
        print("made csv file for saving crawled data\n")
        return f

    def crawl_0(self, id, url, headers=""):
        soup = self.get_request(url, headers=headers)

        table = soup.find("table", attrs={"class":"table table-striped table-hover table-bordered"})
        tbody = table.select_one('tbody')
        trs = tbody.select('tr')

        table_name = "company"
        cols = ["name", "address", "type", "owner"]
        f = self.set_txt(id, table_name, cols)
        for tr in trs:
            name = tr.select('td')[0].text.strip()
            address = tr.select('td')[1].text.strip()
            type = tr.select('td')[2].text.strip()
            owner = tr.select('td')[3].text.strip()
            f.write(name+"|"+address+"|"+type+"|"+owner+"\n")            
        f.close()

    def crawl_1(self, id, url, headers=""):
        soup = self.get_request(url, headers=headers)
        frame = soup.find('iframe', attrs={"class":"iframe-class"})

        frame_soup = self.get_request(frame['src'])
        frame2 = frame_soup.find('frame')

        table_name = "company"
        cols = ["name", "description"]
        f = self.set_txt(id, table_name, cols)

        # selenuim으로 기업명 저장 및 기업명 클릭 후 상세 설명 저장
        self.driver.get(frame2['src'])
        sample = self.driver.find_elements(By.CLASS_NAME, "ex")
        for item in sample:
            f.write(item.text.strip()+"|") # 기업명 저장
            item.send_keys('\n') # 클릭
            time.sleep(2)
            desc = self.driver.find_element(By.XPATH, '//*[@id="profileTab"]/div')
            f.write(desc.text.replace("\n"," ")+"\n") # 기업 상세 설명 저장
        f.close()        

    def crawl_2(self, idx, url, headers=""):
        self.get_request(url, headers)
        cookieBtn = self.driver.find_element(By .XPATH, '//*[@id="didomi-notice-agree-button"]').click()

        gridBox = self.driver.find_element(By .XPATH, '//*[@id="content"]/div/div[1]/section[6]/div/div/div/div[3]/div/div/div')
        gridElements = gridBox.find_elements(By .CLASS_NAME, 'ex_name')
        
        table_name = "company"
        cols = ["name"]
        f = self.set_txt(idx, table_name, cols)
        for gridElement in gridElements:
            f.write(gridElement.text+"\n")
        f.close()

# crawler = Crawler()
# crawler.set_request("hello")

# test= "test_"+"0"
# tester = getattr(crawler, test)
# tester()