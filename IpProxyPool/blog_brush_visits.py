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

def get_proxyer():
    f = open('./useful.txt', 'rb')
    opener_list = []
    for line in f.readlines():
        line = json.dumps(line)
        print(line, type(line))
        proxy_ip = {line.get('type'): line.get('host')}
        proxy_support = request.ProxyHandler(proxy_ip)
        opener = request.build_opener(proxy_support)
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
        opener_list.append(request.install_opener(opener))
    return opener_list

def brush_visits(data, opener_list):
        pass

blog_list_url = 'https://blog.csdn.net/DanielJackZ?spm=1011.2124.3001.5113'
get_blog_list(blog_list_url)

get_proxyer()