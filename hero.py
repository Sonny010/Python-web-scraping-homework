import requests
import json
import time
import random
import os
'''
URL
请求头
json字典转换
'''
url = "https://pvp.qq.com/web201605/js/herolist.json"
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36"}
html = requests.get(url, headers=header)
html.encoding = "utf-8"
json_html = json.loads(html.text)  # json转字典
#print(json_html)
#创建存放图片文件夹
path = r"./hero_pic"
if not os.path.exists(path):
    os.mkdir(path)
    print("目录创建成功")
else:
    print("文件夹已存在")

#生成txt同时写入json内需要爬取信息
with open(path+'//'+'英雄信息.txt', "w", encoding="utf-8") as file:
   for hero in json_html:
       try:
        message = '英雄:{},技能:{}\n'.format(hero['cname'],hero['skin_name'].split('|'))
        file.write(message)
       except Exception:
           message = '英雄:{},技能:{}\n'.format(hero['cname'],hero['title'])
           file.write(message)
           time.sleep(2)
   print('保存成功')
#图片下载
for hero in json_html:
    try:
        skin_name_list=hero['skin_name'].split('|')#皮肤数量
        for i in range(len(skin_name_list)):#判断数量循环
            save_file_name = path +'//' + str(hero['ename']) + '-' + hero['cname'] + '-' + skin_name_list[i] + '.jpg'
            skin_url = "https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg".format(hero['ename'],hero['ename'],i+1)
            if not os.path.exists(save_file_name):
                with open(save_file_name, "wb") as file:
                    file.write(requests.get(skin_url).content)
                    time.sleep(2)
    except Exception:
            save_file_name = path +'//' + str(hero['ename']) + '-' + hero['cname'] + '-' + hero['title'] + '.jpg'
            skin_url = "https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-1.jpg".format(hero['ename'], hero['ename'])
            if not os.path.exists(save_file_name):
                with open(save_file_name, "wb") as file:
                    file.write(requests.get(skin_url).content)
                    time.sleep(2)



