import os
import json
import urllib
import requests
from cityNumMap import city_num_map


def validate_city(city):
    """校验输入的城市参数

    Args:
        city (string): 查找职位的城市

    Raises:
        BaseException: 如果没找到对应的城市值
    """
    if city_num_map.get(city) == 0:
        return
    if city and not city_num_map.get(city):
        raise BaseException('未找到对应城市的信息，请确认后在次输入')

def validate_key_world(key_world):
    """校验职位参数

    Args:
        key_world (string): 职位

    Raises:
        BaseException: 输入参数为空
    """
    if not key_world:
        raise BaseException('输入参数不能为空')

def get_city_num_by_name(city_name):
    """城市名

    Args:
        city_name (string): 城市名

    Returns:
        string: 城市名称对应的值
    """
    city_num = city_num_map.get(city_name)
    return city_num

def get_request_params(city, city_num):
    """获取请求参数

    Args:
        city (string): 城市名
        city_num (number): 城市名称对应的值

    Returns:
        string, string, dict: req_url, ajax_url, headers
    """
    req_url = 'https://www.lagou.com/jobs/list_{}/p-city_{}?&cl=false&fromSearch=true&labelWords=&suginput='.format(urllib.parse.quote(city), city_num)
    ajax_url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false'.format(urllib.parse.quote(city))
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://www.lagou.com/jobs/list_{}/p-city_{}?px=default#filterBox".format(urllib.parse.quote(city), city_num),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    }
    return req_url, ajax_url, headers

def get_params(pn, kd):
    """获取请求参数

    Args:
        pn (number): 页码
        kd (string): 职位

    Returns:
        dict: {
        'first': 'true',
        'pn': pn,
        'kd': kd
    }
    """
    return {
        'first': 'true',
        'pn': pn,
        'kd': kd
    }

def get_cookie(city):
    """获取请求 cookie

    Args:
        city (string): 城市名称

    Returns:
        string: cookie
    """
    city_num = get_city_num_by_name(city)
    req_url, _, headers = get_request_params(city, city_num)
    s = requests.session()
    s.get(req_url, headers=headers, timeout=3)
    cookie = s.cookies
    return cookie

def get_page_info(city, key_world):
    """获取分页信息

    Args:
        city (string): 城市
        key_world (string): 职位

    Returns:
        number: 总页码
    """
    params = get_params(1, key_world)
    city_num = get_city_num_by_name(city)
    _, ajax_url, headers = get_request_params(city, city_num)
    html = requests.post(ajax_url, data=params, headers=headers, cookies=get_cookie(city), timeout=5)
    result = json.loads(html.text)
    total_count = result.get('content').get('positionResult').get('totalCount')
    page_size = result.get('content').get('pageSize')
    page_remainder = total_count % page_size
    total_size = total_count // page_size
    if page_remainder == 0:
        total_size = total_size
    else:
        total_size = total_size + 1
    print('>>>该职位总计{}条数据'.format(total_size))
    return total_size

def get_page_data(city, key_world, total_size):
    """获取搜索数据

    Args:
        city (string): 城市
        key_world (string): 职位
        total_size (number): 总页码
    """
    path = os.path.dirname(__file__)
    path = os.path.join(path, 'lagou.txt')
    f = open(path, mode='w+')
    city_num = get_city_num_by_name(city)
    _, ajax_url, headers = get_request_params(city, city_num)
    for i in range(1, total_size):
        print('>>>开始获取第{}页数据'.format(i))
        params = get_params(i, key_world)
        html = requests.post(ajax_url, data=params, headers=headers, cookies=get_cookie(city), timeout=5)
        result = json.loads(html.text)
        data = result.get('content').get('positionResult').get('result')
        page_size = result.get('content').get('pageSize')
        for i in range(page_size):
            company_name = data[i].get('companyFullName')
            company_size = data[i].get('companySize')
            company_label = data[i].get('companyLabelList')
            salary = data[i].get('salary')
            education = data[i].get('education')
            result_str = '{}&&{}&&{}&&{}&&{}\n'.format(company_name, company_size, company_label, salary, education)
            f.write(result_str)
    print('>>>数据获取完成')

if __name__ == "__main__":
    # 如果没有输入城市信息则默认为全国
    city = input('>>>请输入你要搜索职位的城市：').strip() or "全国"
    validate_city(city)
    kb = input('>>>请输入你要搜索的职位：').strip()
    validate_key_world(kb)
    total_size = get_page_info(city, kb)
    get_page_data(city, kb, total_size)