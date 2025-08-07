import os
import pandas as pd
from flask import Flask, render_template, request
from datetime import datetime


# ルートから起動されるため、scriptsが見えるようになる
from scripts.fetch_data import fetch_weather_data

app = Flask(__name__)

VALID_YEARS = list(range(1979, datetime.now().year + 1))

# 地域と緯度経度の対応表
# 47都道府県とその代表地点（県庁所在地）の緯度・経度
LOCATION_COORDS = {
    "Hokkaido": (43.06417, 141.34694),
    "Aomori": (40.82444, 140.74000),
    "Iwate": (39.70361, 141.15250),
    "Miyagi": (38.26889, 140.87194),
    "Akita": (39.71861, 140.10250),
    "Yamagata": (38.24056, 140.36333),
    "Fukushima": (37.75000, 140.46778),
    "Ibaraki": (36.34139, 140.44667),
    "Tochigi": (36.56583, 139.88361),
    "Gunma": (36.39111, 139.06083),
    "Saitama": (35.85694, 139.64889),
    "Chiba": (35.60472, 140.12333),
    "Tokyo": (35.6895, 139.6917),
    "Kanagawa": (35.44778, 139.64250),
    "Niigata": (37.90222, 139.02361),
    "Toyama": (36.69528, 137.21139),
    "Ishikawa": (36.59444, 136.62556),
    "Fukui": (36.06528, 136.22194),
    "Yamanashi": (35.66389, 138.56833),
    "Nagano": (36.65139, 138.18111),
    "Gifu": (35.39111, 136.72222),
    "Shizuoka": (34.97694, 138.38306),
    "Aichi": (35.18028, 136.90667),
    "Mie": (34.73028, 136.50861),
    "Shiga": (35.00444, 135.86833),
    "Kyoto": (35.02139, 135.75556),
    "Osaka": (34.6937, 135.5023),
    "Hyogo": (34.69139, 135.18306),
    "Nara": (34.68528, 135.83278),
    "Wakayama": (34.22611, 135.16750),
    "Tottori": (35.50361, 134.23833),
    "Shimane": (35.47222, 133.05056),
    "Okayama": (34.66167, 133.93500),
    "Hiroshima": (34.39639, 132.45944),
    "Yamaguchi": (34.18583, 131.47139),
    "Tokushima": (34.06583, 134.55944),
    "Kagawa": (34.34028, 134.04333),
    "Ehime": (33.84167, 132.76611),
    "Kochi": (33.55972, 133.53111),
    "Fukuoka": (33.60639, 130.41806),
    "Saga": (33.24944, 130.29889),
    "Nagasaki": (32.74472, 129.87361),
    "Kumamoto": (32.78972, 130.74167),
    "Oita": (33.23806, 131.61250),
    "Miyazaki": (31.91111, 131.42389),
    "Kagoshima": (31.56028, 130.55806),
    "Okinawa": (26.2125, 127.68111)
}


def load_data(location, years):
    monthly_data = {}
    for year in years:
        filepath = f"data/raw/{location}/{year}.csv"

        if not os.path.exists(filepath):
            lat, lon = LOCATION_COORDS.get(location, (None, None))
            if lat is None:
                return None, f"地域「{location}」の緯度経度が不明です"
            ok, err = fetch_weather_data(lat, lon, year, location)
            if not ok:
                return None, err

        df = pd.read_csv(filepath)
        df["time"] = pd.to_datetime(df["time"])
        df["month"] = df["time"].dt.month

        monthly_avg = df.groupby("month").agg({
            "temperature_2m_mean": "mean",
            "precipitation_sum": "sum"
        }).rename(columns={
            "temperature_2m_mean": f"{year}_temp",
            "precipitation_sum": f"{year}_rain"
        })

        monthly_data[year] = monthly_avg

    result = pd.concat(monthly_data.values(), axis=1)
    return result, None


def load_daily_data(location, years, month):
    daily_data = {}

    for year in years:
        filepath = f"data/raw/{location}/{year}.csv"

        if not os.path.exists(filepath):
            lat, lon = LOCATION_COORDS.get(location, (None, None))
            if lat is None:
                raise ValueError(f"{location} の緯度経度が不明です")
            success, error = fetch_weather_data(lat, lon, year, location)
            if not success:
                raise ValueError(error)

        df = pd.read_csv(filepath)
        df["time"] = pd.to_datetime(df["time"])
        df_month = df[df["time"].dt.month == month].copy()

        # 日番号（1日〜31日）でインデックス化
        df_month["day"] = df_month["time"].dt.day
        df_month.set_index("day", inplace=True)

        # 不足値（例：29日がないなど）への対応
        df_month = df_month[["temperature_2m_mean", "precipitation_sum"]]
        daily_data[year] = df_month

    return daily_data


@app.route('/')
def index():
    location = request.args.get('location', 'Tokyo')
    selected_years = request.args.getlist('years')
    mode = request.args.get('mode', 'monthly')
    selected_month = request.args.get('month', default=3, type=int)

    try:
        years = [int(y) for y in selected_years if int(y) in VALID_YEARS]
    except ValueError:
        return render_template("index.html", location=location, valid_years=VALID_YEARS,
                               selected_years=selected_years, location_list=list(
                                   LOCATION_COORDS.keys()),
                               mode=mode, selected_month=selected_month,
                               error="年の形式が不正です", labels=[], temp_data=[], rain_data=[])

    if not years:
        return render_template("index.html", location=location, valid_years=VALID_YEARS,
                               selected_years=selected_years, location_list=list(
                                   LOCATION_COORDS.keys()),
                               mode=mode, selected_month=selected_month,
                               error="1つ以上の有効な年を選択してください", labels=[], temp_data=[], rain_data=[])

    try:
        if mode == "daily":
            data_by_day = load_daily_data(location, years, selected_month)
            print("✅ data_by_day:", data_by_day)  # ← ここ

            labels = sorted(set(day for df in data_by_day.values()
                            for day in df.index))
            print("✅ labels:", labels)  # ← ここ

            print("📅 日ラベル:", labels)
            print("🌡 気温データ:", temp_data)
            print("☔ 降水データ:", rain_data)

            temp_data = []
            rain_data = []

        for year, df in data_by_day.items():
            temp_data[year] = []
            rain_data[year] = []
            for day in labels:
                try:
                    temp = df["temperature_2m_mean"].loc[day]
                except KeyError:
                    temp = None
                try:
                    rain = df["precipitation_sum"].loc[day]
                except KeyError:
                    rain = None
                temp_data[year].append(temp)
                rain_data[year].append(rain)

        else:  # monthly
            df, error = load_data(location, years)
            if error:
                return render_template("index.html", location=location, valid_years=VALID_YEARS,
                                       selected_years=selected_years, location_list=list(
                                           LOCATION_COORDS.keys()),
                                       mode=mode, selected_month=selected_month,
                                       error=error, labels=[], temp_data=[], rain_data=[])

            labels = [f"{int(m)}月" for m in df.index]
            temp_data = []
            rain_data = []
            for col in df.columns:
                if "_temp" in col:
                    temp_data.append({"label": col.replace(
                        "_temp", ""), "data": list(df[col]), "borderWidth": 2})
                if "_rain" in col:
                    rain_data.append({"label": col.replace(
                        "_rain", ""), "data": list(df[col]), "borderWidth": 2})

    except Exception as e:
        return render_template("index.html", location=location, valid_years=VALID_YEARS,
                               selected_years=selected_years, location_list=list(
                                   LOCATION_COORDS.keys()),
                               mode=mode, selected_month=selected_month,
                               error=f"処理中にエラーが発生しました: {e}", labels=[], temp_data=[], rain_data=[])

    return render_template("index.html", labels=labels, temp_data=temp_data, rain_data=rain_data,
                           location=location, valid_years=VALID_YEARS, selected_years=selected_years,
                           location_list=list(LOCATION_COORDS.keys()), mode=mode, selected_month=selected_month,
                           error=None)
