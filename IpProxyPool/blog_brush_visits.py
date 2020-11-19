import requests
from bs4 import BeautifulSoup

def get_blog_list(blog_list_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'
    }
    html = requests.get(blog_list_url, headers=headers).text
    soup = BeautifulSoup(html)
    res = soup.findAll('h4')
    print(res)

blog_list_url = 'https://blog.csdn.net/DanielJackZ?spm=1011.2124.3001.5113'
get_blog_list(blog_list_url)