import advertools as adv
# import pandas as pd
# # bbc_sitemap = adv.sitemap_to_df('http://www.cettire.com/robots.txt', recursive=False)
# # print(bbc_sitemap.head(10))
# adv.crawl('https://www.indiehackers.com', 'indiehackers'+'-adv.jl',
                            #   follow_links=True, exclude_url_params=True)



from usp.objects.page import (
    SitemapPage,
    SitemapNewsStory,
    SitemapPageChangeFrequency,
)
from usp.objects.sitemap import (
    IndexRobotsTxtSitemap,
    PagesXMLSitemap,
    IndexXMLSitemap,
    InvalidSitemap,
    PagesTextSitemap,
    IndexWebsiteSitemap,
    PagesRSSSitemap,
    PagesAtomSitemap,
)
from usp.tree import sitemap_tree_for_homepage
tree = sitemap_tree_for_homepage('http://www.cettire.com')
# tree = IndexXMLSitemap('https://www.indiehackers.com/')
# all_pages() returns an Iterator
print('=======\n',tree)
for page in tree.all_pages():
    print(page.url)
robot=tree.sub_sitemaps[0].url
# indexxmlsimap=[ x.url for x in tree.sub_sitemaps[0].sub_sitemaps]
# print('========\n',indexxmlsimap)

# adv.crawl('https://dogsexdolls.com', 'my_output_file.jl', follow_links=True)
# crawl_df = pd.read_json('my_output_file.jl', lines=True)
# print(crawl_df['url'].tolist())

# from click.testing import CliRunner
# from shot_scraper import cli
# print('---')
# runner = CliRunner()
# result = runner.invoke(cli.cli, ["shot","www.baidu.com"])
# result = runner.invoke(cli.cli, ["shot","www.baidu.com","--width 412", "--height 915"])
# result = runner.invoke(cli.cli, ["shot","www.baidu.com --width 412  --height 915"])

# result = runner.invoke(cli.cli, ["shot", "pdf","www.baidu.com"])
# result = runner.invoke(cli.cli, ["shot", "pdf  www.baidu.com"])



# import optparse
# import asyncio

# from datetime import datetime
# from datetime import timedelta
# from unittest import result
# from urllib.parse import quote_plus
# import requests
# import math
# import os
# import random
# import time
# import platform
# import json
# from playwright.async_api import async_playwright




# async def get_playright(proxy:bool=False,headless:bool=True):
#     print('proxy',proxy,'headless',headless)
#     browser=''
#     if 'linux' in platform.system():
#         headless=True
#     playwright =await  async_playwright().start()
#     PROXY_SOCKS5 = "socks5://127.0.0.1:1080"
#     # browser=''
#     if proxy==False:
#         try:
#             print("start pl without proxy")
#             browser = await  playwright.firefox.launch(headless=headless)
#             print('start is ok')
#             return browser

#         except:
#             print('pl no proxy start failed')
#             browserLaunchOptionDict = {
#             "headless": headless,
#             "proxy": {
#                     "server": PROXY_SOCKS5,
#             }
#             } 
#             browser = await playwright.firefox.launch(**browserLaunchOptionDict)
#             # Open new page    
#             return browser
#     else: 
#         print('proxy===',headless)
#         browserLaunchOptionDict = {
#         "headless": headless,
#         "proxy": {
#                 "server": PROXY_SOCKS5,
#         }
#         } 
#         browser = await playwright.firefox.launch(**browserLaunchOptionDict)
#         # Open new page    

#         return browser

# def url_ok(url):
#     try:
#         response = requests.head(url)
#     except Exception as e:
#         # print(f"NOT OK: {str(e)}")
#         return False
#     else:
#         if response.status_code == 400 or response.status_code==404:
#             # print("OK")
#             print(f"NOT OK: HTTP response code {response.status_code}")

#             return False
#         else:

#             return True   


# async def coldstart(topic,table):
#     item_list = []
#     datall=[]

#     start = time.time()
#     url = "https://dogsexdolls.com"
#     try:
#         browser = await get_playright(True,False)
#         context = await browser.new_context()
#         page = await browser.new_page()
#         print('this url',url)
#         await page.set_viewport_size({"width": 412, "height": 915})
#         res=await page.goto(url)
#         print('user home url',url)
        
#         await page.emulate_media(media="screen")
#         await page.pdf(path="page.pdf")
#     except:
#         pass
# asyncio.run(coldstart('',''))