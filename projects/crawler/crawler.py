# -*- coding: utf-8 -*-
"""
简单爬虫程序 - 爬取 quotes.toscrape.com 名言
"""

import requests
from bs4 import BeautifulSoup


def crawl_quotes():
    """
    爬取名言网站首页的名言和作者
    """
    url = "http://quotes.toscrape.com/"
    
    # 1. 发送HTTP请求
    response = requests.get(url)
    response.encoding = 'utf-8'
    
    # 2. 解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 3. 提取名言和作者
    quotes = soup.select('.quote')
    
    print(f"共找到 {len(quotes)} 条名言\n")
    
    for i, quote in enumerate(quotes, 1):
        text = quote.select_one('.text').get_text()
        author = quote.select_one('.author').get_text()
        print(f"{i}. {text}")
        print(f"   —— {author}\n")


if __name__ == "__main__":
    crawl_quotes()
