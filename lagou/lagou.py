import os
import json
import urllib
import requests


def get_request_params(position, city=215):
    req_url = 'https://www.lagou.com/jobs/list_{}/p-city_{}?&cl=false&fromSearch=true&labelWords=&suginput='.format(urllib.parse.quote(position), city)
    ajax_url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false'.format(urllib.parse.quote('深圳'))
    headers = headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://www.lagou.com/jobs/list_{}/p-city_{}?px=default#filterBox".format(urllib.parse.quote(position), city),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    }
    return req_url, ajax_url, headers

def get_params(pn, kd):
    return {
        'first': 'true',
        'pn': pn,
        'kd': kd
    }

def get_cookie(position):
    req_url, _, headers = get_request_params(position)
    s = requests.session()
    s.get(req_url, headers=headers, timeout=3)
    cookie = s.cookies
    return cookie

def get_page_info(position, key_world):
    params = get_params(1, key_world)
    _, ajax_url, headers = get_request_params(position)
    html = requests.post(ajax_url, data=params, headers=headers, cookies=get_cookie(position), timeout=5)
    result = json.loads(html.text)
    total_count = result.get('content').get('positionResult').get('totalCount')
    page_size = result.get('content').get('pageSize')
    page_remainder = total_count % page_size
    total_size = total_count // page_size
    if page_remainder == 0:
        total_size = total_size
    else:
        total_size = total_size + 1
    print(total_size)
    return total_size, page_size

def get_page_data(position, key_world, total_size, page_size):
    path = os.path.dirname(__file__)
    path = os.path.join(path, 'lagou.txt')
    f = open(path, mode='w+')
    _, ajax_url, headers = get_request_params(position)
    for i in range(1, total_size):
        print('>>>开始获取第{}页数据'.format(i))
        params = get_params(i, key_world)
        html = requests.post(ajax_url, data=params, headers=headers, cookies=get_cookie(position), timeout=5)
        result = json.loads(html.text)
        data = result.get('content').get('positionResult').get('result')
        for i in range(page_size):
            company_name = data[i].get('companyFullName')
            company_size = data[i].get('companySize')
            company_label = data[i].get('companyLabelList')
            salary = data[i].get('salary')
            education = data[i].get('education')
            result_str = '{}&&{}&&{}&&{}&&{}\n'.format(company_name, company_size, company_label, salary, education)
            f.write(result_str)
    print('>>>数据获取成功')

if __name__ == "__main__":
    position = input('请输入你要搜索职位的城市：')
    kb = input('请输入你要搜索的职位：')
    total_size, page_size = get_page_info(position, kb)
    get_page_data(position, kb, total_size, page_size)