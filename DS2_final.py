# 横浜市の12月の気象情報

import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import datetime

db_name = 'weather.sqlite'

def scraping(url, date):
    # スクレイピング対象のurl
    url = "https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=46&block_no=47670&year=2023&month=12&day=&view=p1"

    r  = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.find_all('tr', class_='mtx')

    # 見出しの削除
    rows = rows[3:]

    # 日毎の気象データを配列に格納
    weather_data = []

    # 月毎に分割
    for row in rows:
        items = row.find_all('td')

        # 降水量(mm)
        if len(items) >= 3:
            rainfall = items[3].text.strip()
        # 気温(℃)
        if len(items) >= 6:
            temperature = items[6].text.strip()
        # 湿度(%)
        if len(items) >= 9:
            humidity = items[9].text.strip()
        # 日照時間(h)
        if len(items) >= 16:
            sunshine_hours = items[16].text.strip()
        time.sleep(0.5)

        d_weather = {   'rainfall' : rainfall,
                        'temperature' : temperature,
                        'humidity' : humidity,
                        'sunshine_hours' : sunshine_hours
                    }
        weather_data.append(d_weather)

    return weather_data
# DBに接続
#con = sqlite3.connect(db_name)
#cur = con.cursor()

# テーブルの作成
#cur.execute('CREATE TABLE D_weathers(rainfall text, temperature text, hunidity text, sunshine_hours text);')
# データの挿入
#insert_data = "INSERT INTO D_weathers VALUES (?, ?, ?, ?);"
#cur.executemany(insert_data, weather_data)

#cur.execute()

#con.close()

