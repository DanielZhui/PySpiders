import os
import json
import requests
from lxml import etree
from urllib import request

def get_blog_list(blog_list_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'
    }
    html = requests.get(blog_list_url, headers=headers).text
    selector = etree.HTML(html)
    data = selector.xpath('//*[@id="articleMeList-blog"]/div[2]/div//a/@href')
    return data

def brush_visits(data):
    f = open(os.path.join(os.path.dirname(__file__), 'useful.txt'))
    for line in f.readlines():
        line = json.loads(line)
        proxy_ip = {line.get('type'): line.get('host')}
        print('>>>', proxy_ip)
        proxy_support = request.ProxyHandler(proxy_ip)
        opener = request.build_opener(proxy_support)
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
        for link in data:
            print('brush>>>', link)
            request.urlopen(link)


blog_list_url = 'https://blog.csdn.net/DanielJackZ?spm=1011.2124.3001.5113'
data = get_blog_list(blog_list_url)
brush_visits(data)