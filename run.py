from src.combinated_crawler import Crawler
from src.db_connecter import DB
from apscheduler.schedulers.blocking import BlockingScheduler

def crawling(cur_idx):
    url = urls.loc[cur_idx, 'url']
    headers = urls.loc[cur_idx, 'headers']
    id = urls.loc[cur_idx, 'id']
    func_name = "crawl_"+str(id) #website id와 crawler 함수 이름 일치
    website_crawler = getattr(crawler, func_name)
    website_crawler(cur_idx, url, headers)

    # db.insert_data(cur_id)
    
def circuit():
    for i in range(len(urls)):
        for retry in range(2): #에러 발생시 재시도 횟수
            try:
                crawling(i)
                print("finished crawling for website index " +str(i)+"\n")
                break
            except:
                print("failed crawling for website index " +str(i)+"\n")
            
      
if __name__ == "__main__":
    crawler = Crawler()
    db = DB()
    urls = db.read_url()
    
    sched = BlockingScheduler(timezone='Asia/Seoul')
    sched.add_job(circuit, 'cron', hour=0, minute=20) #매일 hour시 minute분에 실행
    sched.start()

