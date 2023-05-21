import pymysql
import pymysql.cursors
from dotenv import load_dotenv
import os 
import pandas as pd

class DB:
    def __init__(self) -> None:
        load_dotenv()
        host = os.environ.get('DB_HOST')
        user = os.environ.get('DB_USER')
        pwd = os.environ.get('DB_PASSWORD')
        dbname = os.environ.get('DB_NAME')
        self.conn = pymysql.connect(host=host, user=user, password=pwd, db=dbname, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()
        print("loaded DB\n")

    def read_url(self):
        query = "SELECT * FROM website"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.urls = pd.DataFrame(rows)
        print("got data from website table\n")
        return self.urls

    def insert_data(self, id):
        f_name = str(id)+".txt"
        f = open(f_name, 'r', encoding='utf-8')

        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if i==0:
                table = line.strip()
            elif i==1:
                # cols = line.split(' ')
                line = line.strip()
                datas = line.split('|')
                cols = ",".join(datas)
                col_len = len(datas)
            else:
                line = line[:-1]
                datas = line.split('|')
                query = "INSERT INTO "+table+" ("+cols+") VALUES("
                for j in range(col_len):
                    query = query + "%s"
                    if j==col_len-1:
                        query = query + ");"
                    else:
                        query = query + ", "
                try:
                    self.cursor.execute(query, tuple(datas))
                except:
                    self.cursor.execute(query, "|".join(datas))
        self.conn.commit()
        print("inserted data to "+table+" table\n")
        # self.connect.close()

