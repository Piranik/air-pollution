from ckan_crawl.ckan_crawl import CrawlCKAN
from config_utils.config import ConfigCrawlYaml

#get config
configInst=ConfigCrawlYaml()
config=configInst.get_config()

#do work
cc=CrawlCKAN(config)
cc.do_process_all()
