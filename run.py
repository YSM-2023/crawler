from src.combinated_crawler import Crawler
from src.db_connecter import DB

crawler = Crawler()
db = DB()
website_table = db.read_url()

for i in range(len(website_table)):
    id = website_table.loc[i, 'id']
    url = website_table.loc[i, 'url']
    headers = website_table.loc[i, 'headers']
    func_name = "crawl_"+str(id)
    website_crawler = getattr(crawler, func_name)
    website_crawler(id, url, headers)
    print("finished crawling for " +str(id)+ " website\n")

    db.insert_data(i)

