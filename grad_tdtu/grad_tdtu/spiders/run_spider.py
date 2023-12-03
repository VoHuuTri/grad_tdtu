from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process

# Import spider
from grad import GD_DT_Spider

def run_spider(my_param):
    process = CrawlerProcess()

    # Add your spider to the process and pass the parameter
    process.crawl(GD_DT_Spider, my_param=my_param)

    # Start the crawling process
    process.start()

if __name__ == "__main__":
    # Create and start a process for each parameter
    processes = []
    for my_param in range(1,500):
        p = Process(target=run_spider, args=(my_param,))
        p.start()
        # processes.append(p)
        p.join()

    # Wait for all processes to finish
    # for p in processes:
    #     p.join()
