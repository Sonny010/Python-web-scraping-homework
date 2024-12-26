import requests
import json
import time
import random
import os

url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%9C%80%E6%96%B0&page_limit=50"
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36"}


##url循环
pages = 1 #页数
all_movies = []#初始化定义一个列表咯
for page in range(pages):
    page = page * 50 #douban 默认一次50条信息
    url_page = url + f"&page_start={page}" #换页:尾部添加页数
    print(url_page)

    html = requests.get(url_page, headers=header)
    html.encoding = "utf-8"
    json_html = json.loads(html.text)  # json转字典

    if len(json_html.get('subjects', [])) == 0:  # 判断电影数量不为空
        print("没有数据")
        break

    for movie in json_html['subjects']:  # 循环提取电影信息
        movie_rate = {
            'title': movie['title'],
            'rate': movie['rate'],
            'cover': movie['cover']
        }
        all_movies.append(movie_rate)

    delay = random.uniform(2, 5)  # 增加一个2~5秒的等待时间
    time.sleep(delay)
    print(f"爬取完成，等待{delay:.2f}秒")

print(all_movies)
print(f"共爬取电影数量: {len(all_movies)}")

if not os.path.exists(r"./pic"):
    os.mkdir(r"./pic")
    print("目录创建成功")
else:
    print("文件夹已存在")

##以txt存储 电影信息 名字和评分
with open("movie.txt", "w", encoding="utf-8") as f:
    f.write('序号、电影名、评分'+'\n')
    index = 1
    for movie in all_movies:
        f.write(f"{index},{movie['gittitle']},{movie['rate']}\n")
        ##下载图片
        movie_path = './pic/' + str(index)+","+movie['title']+'.jpg'
        index +=1
        if not os.path.exists(movie_path):
            print("新增图片"+movie_path)
            with open(movie_path, 'wb') as file:
                file.write(requests.get(movie['cover']).content)