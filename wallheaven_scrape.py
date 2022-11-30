#!/usr/bin/env python
# coding: utf-8

from getsoup import get_soup
import requests
import os
from pathlib import Path
import numpy as np
import sys

if __name__ == '__main__':

    keyword = "flower"
    
    # 创建keyword目录
    pic_path = Path("./wallhaven/"+keyword)

    if os.path.exists(pic_path)==False:
            os.makedirs("./wallhaven/"+keyword)

    # 查看是否有进度文件
    if os.path.exists(keyword+".npy"):
        names = np.load(keyword+".npy").tolist() # numpy没有pop方法
        print("tiaoguo")
        
    else:                
    
        domain = "https://wallhaven.cc/search?q="+keyword+"&categories=100&purity=100&atleast=2560x1440&ratios=16x9%2C16x10&sorting=relevance&order=desc&page=12"
    
        # 获取页数
        soup = get_soup(domain) 
        page_num = soup.find('header',class_="thumb-listing-page-header").find('h2').get_text().split('/' )[-1]
        page_num = int(page_num)
     
    
        names = [] # 储存图片的数字编号
        for i in range(page_num): 
            # 每页
            soup = get_soup("https://wallhaven.cc/search?q="+keyword+"&categories=110&purity=100&sorting=relevance&order=desc&page="+str(i+1))
        
            div_list = soup.find('section',class_="thumb-listing-page").find_all('li')
            if div_list:
                for dic2 in div_list:
                    name0 = dic2.find("figure").attrs['data-wallpaper-id']
                    names.append(name0)            
            else:
                i = page_num
        np.save(keyword+".npy",np.array(names)) #用于保存进度
    
    
    # 抓取获取图片的src ，并下载
    for i in range(len(names)):    
 
        try:
            
            name = names.pop()
            #print(i,name)
            soup = get_soup('https://wallhaven.cc/w/'+name)     
            src = soup.find("main").find("section").find("img").attrs['src'] #抓取获取图片的src
            # 下载图片
            r = requests.get(src)
            with open("./wallhaven/"+keyword+"/"+name+".jpg", 'wb') as f:      
                f.write(r.content)
        except:
                names3 = np.array(names)
    
                np.save(keyword+".npy",names3)
                
                print("出现异常已保存进度,本次下载照片数量为：",i+1)
                sys.exit() # 异常，保存进度，跳出循环，终止程序
       
                





