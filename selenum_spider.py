from lxml import etree
from selenium import webdriver
import time
import json
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

def wangyiyunSpider(song_type,list1):
    driver = webdriver.Chrome()
    driver.get('https://music.163.com/#/search/m/?id=2624438246&s=%s'%song_type)
    time.sleep(2)
    driver.switch_to.frame('contentFrame')
    pageSource = driver.page_source

    count = 1
    list1,count = getSongInfo(pageSource,list1,count,song_type)


    for i in range(19):
        js="var q=document.documentElement.scrollTop=100000"
        driver.execute_script(js)
        driver.find_element_by_xpath('//div[@id="m-search"]/div[3]/div/a[last()]').click()
        driver.get('https://music.163.com/#/search/m/?id=2624438246&s=%s'%song_type)
        js="var q=document.documentElement.scrollTop=0"
        driver.execute_script(js)
        time.sleep(1)
        driver.switch_to.frame('contentFrame')
        pageSource = driver.page_source
        list1,count = getSongInfo(pageSource,list1,count,song_type)
    driver.close()
    return list1
if __name__ == "__main__":
    list1 = []
    for song_type in ["主题曲","片头曲","片尾曲"]:   #搜索主题曲，片头曲，片尾曲并拿到前20页结果
        list1 = wangyiyunSpider(song_type,list1)
    with open("wangyiyun.json","w") as f:
        f.write(json.dumps(list1))

