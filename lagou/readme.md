# python 爬虫 ==> 获取拉勾招聘信息

## 启动项目：
> python lagou.py
>
> **note:** 数据爬取完成之后同级文件夹中会新建一个 lagou.txt 文件，里面存储爬去到的数据

## 项目说明

### 故事背景

  最近有个好哥们啊浪迫于家里工资太低，准备从北方老家那边来深圳这边找工作，啊浪是学平面设计的知道我在深圳这边于是向我打听深圳这边平面设计薪资水平，当时我有点懵逼这个行业不熟悉啊咋搞呢，准备打开招聘网站先看看再说打开网站输入招聘职位发先量还挺大，这样慢慢看不行啊效率太低啦，咋是程序员啊直接把数据拉下来不就行啦于是有啦这篇博客。



### 技术实现

#### 用到的库

```python
import os
import json
import urllib
import requests
```



#### 页面分析

数据地址：https://www.lagou.com/

当我在 chrom 中输入拉勾网站查看页面源码时发现页面上的数据并没有直接显示在源码上。推断可能是使用 AJAX 异步加载数据，当我打开 chrom 开发者工具在 network 中查看 XHR 时发现一个 `https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false` 请求点开 response 果然数据都在这个请求中返回。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201114100626531.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0RhbmllbEphY2ta,size_16,color_FFFFFF,t_70#pic_center)


返回的数据格式如下：

![\[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-NRpqsHcD-1605319503100)(/Users/wollens/Library/Application Support/typora-user-images/image-20201114094558145.png)\]](https://img-blog.csdnimg.cn/20201114100707660.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0RhbmllbEphY2ta,size_16,color_FFFFFF,t_70#pic_center)


可以发现我们需要的数据都存放在 result 中，于是准备直接获取数据但是使用 request 去模拟请求发现每次都会被拦截。因为拉勾在不登录的情况下浏览器也能获取数据应该不是用户级别的拦截，猜想可能是在 cookie 层面做的限制，发现请求没有携带网站的 cookie 直接拦截

![\[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-XG5ZUG2R-1605319503101)(/Users/wollens/Library/Application Support/typora-user-images/image-20201114095322932.png)\]](https://img-blog.csdnimg.cn/2020111410072817.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0RhbmllbEphY2ta,size_16,color_FFFFFF,t_70#pic_center)


获取请参数

```python
def get_request_params(city, city_num):
    req_url = 'https://www.lagou.com/jobs/list_{}/p-city_{}?&cl=false&fromSearch=true&labelWords=&suginput='.format(urllib.parse.quote(city), city_num)
    ajax_url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false'.format(urllib.parse.quote(city))
    headers = headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://www.lagou.com/jobs/list_{}/p-city_{}?px=default#filterBox".format(urllib.parse.quote(city), city_num),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    }
    return req_url, ajax_url, headers
```



于是在 请求中加上 cookie, 代码如下：

```python
def get_cookie(city):
    city_num = get_city_num_by_name(city)
    req_url, _, headers = get_request_params(city, city_num)
    s = requests.session()
    s.get(req_url, headers=headers, timeout=3)
    cookie = s.cookies
    return cookie
```



虽然加入 cookie 后能获取到数据但每次都是第一页的数据且是固定职位的数据，当再次查看请求真实数据地址的链接发现请求中每次都会携带 query 参数如下：

![\[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-zJOO5Tsv-1605319503103)(/Users/wollens/Library/Application Support/typora-user-images/image-20201114095819061.png)\]](https://img-blog.csdnimg.cn/20201114100750363.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0RhbmllbEphY2ta,size_16,color_FFFFFF,t_70#pic_center)




于是增加请求参数获取：

```python
def get_params(pn, kd):
    return {
        'first': 'true',
        'pn': pn,
        'kd': kd
    }
```



虽然我们解决请求参数以及获取页面数，但是每次只能爬取固定城市的数据太僵硬啦，查找原因原来是我们在请求数据 url 中携带有 city_nun 这个参数，每个城市都有一个对应的数字

![\[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-o0GA9zhy-1605319503104)(/Users/wollens/Library/Application Support/typora-user-images/image-20201114100119917.png)\]](https://img-blog.csdnimg.cn/20201114100819772.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0RhbmllbEphY2ta,size_16,color_FFFFFF,t_70#pic_center)


打开拉勾页面源码将页面拉到最底部会发现 cityNumMap,查找到这个我们就能控制获取想要的城市职位信息啦

![\[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-mE6DcOrQ-1605319503105)(/Users/wollens/Library/Application Support/typora-user-images/image-20201114094941614.png)\]](https://img-blog.csdnimg.cn/20201114100835356.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0RhbmllbEphY2ta,size_16,color_FFFFFF,t_70#pic_center)



### 实现效果
在本地执行 `pythin3 lagou.py` 输入查找的地址以及职位会在当前同级目录下生成 lagou.txt 文件存储数据结果

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201114101255638.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0RhbmllbEphY2ta,size_16,color_FFFFFF,t_70#pic_center)

### 部分结果数据
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201114101327297.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0RhbmllbEphY2ta,size_16,color_FFFFFF,t_70#pic_center)
