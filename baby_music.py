from lxml import etree
from selenium import webdriver
import time
import json
import re
def getSongInfo(pageSource,list1,count,song_type):
    selector = etree.HTML(pageSource)
    songDiv_list = selector.xpath('//div[@class="sn"]')
    for songDiv in songDiv_list:
        song_name2 = songDiv.xpath('.//span/@title')
        try:
            if song_name2 != []:
                dict1 = {}
                song_name1 = songDiv.xpath('.//b/text()')[0]
                if song_name1 == []:
                    song_name1 = songDiv.xpath('.//b/span/text()')[0]
                dict1["song_name"] = song_name1 + " " + song_name2[0].replace("主题曲", "")
                dict1["song_url"] = 'http://music.163.com/song/media/outer/url?id=%s.mp3'%(songDiv.xpath('.//a[1]/@href')[0].split("=")[1])
                dict1["song_num"] = count
                dict1["song_type"] = song_type
                count += 1
                list1.append(dict1)

        except:
            print(song_name2)
    return list1,count

def wangyiyunSpider(url,list1):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    driver.switch_to.frame('contentFrame')
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    pageSource = driver.page_source
    song_ids = re.findall(r'/song\?id=(\d+)',pageSource)
    selector = etree.HTML(pageSource)
    title_list = selector.xpath('//td[2]/div/div/div/span/a/b/@title')
    singer_list = selector.xpath('//td[4]/div/span/@title')
    ablum_list = selector.xpath('//td[5]/div/a/@title')
    print(len(song_ids),len(title_list),len(singer_list),len(ablum_list))
    for i in range(len(song_ids)):
        dict1 = {}
        dict1["song_url"] = 'http://music.163.com/song/media/outer/url?id=%s.mp3'%song_ids[i]
        dict1["song_name"] = title_list[i]
        dict1["song_singer"] = singer_list[i]
        dict1["song_ablum"] = ablum_list[i]
        print(dict1)
        list1.append(dict1)
    driver.close()
    return list1
if __name__ == "__main__":
    list1 = []
    for url in ["https://music.163.com/#/playlist?id=613045129","https://music.163.com/#/playlist?id=2649838653"]:   #搜索主题曲，片头曲，片尾曲并拿到前20页结果
        list1 = wangyiyunSpider(url,list1)
    with open("wangyiyun.json","w") as f:
        f.write(json.dumps(list1))

