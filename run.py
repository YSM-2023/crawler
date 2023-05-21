from src.combinated_crawler import Crawler
from src.db_connecter import DB

crawler = Crawler()
db = DB()
urls = db.read_url()

for i in range(len(urls)):
    url = urls.loc[i, 'url']
    headers = urls.loc[i, 'headers']
    id = urls.loc[i, 'id']
    func_name = "crawl_"+str(id)
    website_crawler = getattr(crawler, func_name)
    website_crawler(i, url, headers)
    print("finished crawling for " +str(i)+ " website\n")

    db.insert_data(i)

