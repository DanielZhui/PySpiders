# 构建 ip 代理池

## 启动项目：
> python proxy_pool.py
>
> **note:** 数据爬取完成之后同级文件夹中会新建一个 useful.txt 文件，里面存储k可用 ip 信息（注意源数据需要梯子才能获取否则可能会出现超时）

### ip 代理池应用：刷博客访问量
- 先启动 `proxy_pool.py` 获取可用 `ip` 代理
> python proxy_pool.py
- 在启动 `brush_blog_visits.py `(在启动项目之前可以将 `blog_list_url` 换成自己的博客列表 `url`)
> python brush_blog_visits.py
