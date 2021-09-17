import requests,sys
from bs4 import BeautifulSoup
import time
import socket

target="http://book.sfacg.com/Novel/188859/MainIndex/"
print('页面抓取中……')
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
mypath='D:\\TXT小说\\'
bookserver='http://book.sfacg.com/'
html=requests.get(target,headers=headers)
time.sleep(1)
html.encoding="UTF-8"

texts=BeautifulSoup(html.text,'lxml')
bookname=texts.find('h1').get_text()
booklinks=texts.find('div',class_='catalog-list')
booknum=len(booklinks)
print('开始下载小说：《'+bookname+'》，共有 '+str(booknum)+' 章节。')

i=0
with open(mypath+bookname+'.txt','a+',encoding='GBK') as ok:
    ok.write(bookname+'\n=====================================\n')
    ok.close()

    for zjlink in booklinks:
       html2=requests.get(bookserver+zjlink['href'],headers=headers)
       time.sleep(2)
       html2.encoding='UTF-8'
       texts2=BeautifulSoup(html2.text,'lxml')
       mytext=texts2.find('div',id='content')
       mytext=mytext.text.replace('\xa0'*4,'\n')
       mytext=mytext.replace('\n\n','\n')
    mytext=mytext.replace('X小说网 WWW.XX，最快更新'+bookname+'最新章节！','')
    with open(mypath+bookname+'.txt','a+', encoding='GBK') as ok:
        ok.write('-----------------------\n'+zjlink.string+'\n--------------------')
        try:
            ok.writelines(mytext)
            ok.write('\n')
            i+=1
            sys.stdout.write("已下载:%.2f%%" % float(i/booknum*100) + '\r')
            sys.stdout.flush()
            #print(bookname+'：'+zjlink.string+'下载完成！')
        except:
            ok.writelines(zjlink.string+'下载失败！')
            ok.write('\n')
            i+=1
            sys.stdout.write("已下载:%.2f%%" % float(i/booknum*100) + '\r')
            sys.stdout.flush()
            print(bookname+'：'+zjlink.string+'下载失败！XXXXXXXXXXX')
print('-------------------\n'+bookname+'下载完成！\n-----------------')
