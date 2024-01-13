import json
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import pymysql

# 指定Chrome驱动程序的路径
driver_path = './driver/chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# 创建Chrome浏览器的一个实例，并指定驱动程序路径
service = ChromeService(executable_path=driver_path)
chrome = webdriver.Chrome(service=service)


def insertData(song_data):
    conn = pymysql.connect(host='localhost', user='root', password='neo1991', db='music', charset='utf8mb4')
    # 创建游标对象
    cursor = conn.cursor()
    try:
        # 插入数据
        for item in song_data:
            item['favShow'] = item['favShow'].replace('w+', '0000')
            item['listenCount'] = item['listenCount'].replace('w+', '0000')
            select_query = """
                    SELECT COUNT(*) FROM singer_data_now WHERE song_id = %s AND date_time = %s
                """
            # 执行查询语句
            cursor.execute(select_query, (item['id'], datetime.now().strftime("%Y-%m-%d")))
            # 获取查询结果
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.execute("""
                INSERT INTO singer_data_now (
                    song_id, singer, name, fav_show, listen_count, top_score, grand_score, 
                    now_listener, today_index, today_rank, date_time, create_time
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                    item['id'], item['allSingers'], item['name'], item['favShow'], item['listenCount'],
                    item['topScore'], item['grandScore'], item['nowListener'], item['todayIndex'],
                    item['todayRank'], datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
        # 提交事务
        conn.commit()
        print("数据插入成功")

    except Exception as e:
        # 发生错误时回滚
        conn.rollback()
        print("数据插入失败:", str(e))

    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()


# 打开网站
url = 'https://tool.curleyg.info'
chrome.get(url)
data = []
singers = ['周杰伦','邓紫棋','林俊杰','薛之谦','汪苏泷','陈奕迅','李荣浩','周深','张杰','许嵩']

for j in range(len(singers)):
    for i in range(20):
        try:
            while True:
                response = requests.get(
                    'https://tool.curleyg.info/Collect?keyword='+singers[j]+'&pageIndex=' + str(i),
                    verify=False)
                if response.status_code == 200:
                    data = json.loads(response.content)['data']
                    if data[0]['nowListener'] != 0:
                        insertData(data)
                        print(singers[j] + 'success: ' + str(i))
                        break
                else:
                    print(singers[j] + 'retrying:' + str(i))
        except Exception as e:
            print(e)

quit()
