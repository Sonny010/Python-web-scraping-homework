import requests
import json


url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%9C%80%E6%96%B0&page_limit=50&page_start=0"
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
html = requests.get(url, headers=header)
#tml.text)print(h
json_html = json.loads(html.text)
movies = json_html["subjects"][0]
rate =  movies["rate"]
title = movies["title"]
print("分数：" +str(rate) + ", 名字：" + str(title))