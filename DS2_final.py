# 横浜市の12月の気象情報

import requests
from bs4 import BeautifulSoup
import sqlite3
import time

db_name = 'weather.sqlite'

def str2float_z(str):
    try:
        return float(str)
    except:
        return 0.0
    
url = "https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=46&block_no=47670&year=2023&month=12&day=&view="

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.aprser')
rows = soup.find_all('tr', class_='mtx')

# 見出しの削除
rows = rows[:3]

# 日付ごとの気象データを配列に格納
weather_data = []

# 必要な気象情報のスクレイピング
for row in rows:
    items = row.find_all('td')
    if len(items) >= 3:
        # 日付
        date = items[0].text.strip()
        # 降水量
        rainfall = str2float_z(items[3].text.strip())
        # 気温
        temperature = items[6].text.strip()
        # 湿度
        humidity = items[9].text.strip()
        # 日照時間
        sunshine_hours = items[16].text.strip()

        weather_data.append((date, rainfall, temperature, humidity, sunshine_hours))
time.sleep(0.5)

# DBに接続
con = sqlite3.connect(db_name)
cur = con.cursor()

# テーブルの作成
cur.execute('''CREATE TABLE IF NOT EXISTS D_weathers(
                date TEXT,
                rainfall REAL, 
                temperature REAL, 
                humidity REAL, 
                sunshine_hours REAL
                )''')

# データの挿入
sql_insert = '''INSERT INTO D_weathers(
                date, rainfall, temperature, humidity, sunshine_hours) 
                VALUES (?, ?, ?, ?, ?)'''

cur.executemany(sql_insert, weather_data)

# コミット処理
con.commit()

# 接続を閉じる
con.close()