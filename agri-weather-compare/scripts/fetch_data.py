# 気象データを取得するスクリプト
# scripts/fetch_data.py

import requests
import os
import pandas as pd


def fetch_weather_data(lat, lon, year, location_name):
    url = "https://archive-api.open-meteo.com/v1/archive"
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_mean", "precipitation_sum"],
        "timezone": "Asia/Tokyo"
    }

    print(f"📡 {location_name} {year}年のデータを取得中...")

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()["daily"]
        df = pd.DataFrame(data)
        output_dir = f"data/raw/{location_name}"
        os.makedirs(output_dir, exist_ok=True)
        filepath = f"{output_dir}/{year}.csv"
        df.to_csv(filepath, index=False)
        print(f"✅ 保存しました: {filepath}")
        return True, None
    else:
        return False, f"❌ データ取得に失敗しました（{response.status_code}）"
