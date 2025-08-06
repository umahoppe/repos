# ルーティングをここに記述
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    # データ読み込み
    df = pd.read_csv("data/processed/Tokyo/monthly_comparison.csv")
    labels = [f"{int(m)}月" for m in df["month"]]

    # 折れ線グラフ用：気温
    temp_data = []
    for col in df.columns:
        if "_temp" in col:
            temp_data.append({
                "label": col.replace("_temp", ""),
                "data": list(df[col]),
                "borderWidth": 2
            })

    # 棒グラフ用：降水量
    rain_data = []
    for col in df.columns:
        if "_rain" in col:
            rain_data.append({
                "label": col.replace("_rain", ""),
                "data": list(df[col]),
                "borderWidth": 2
            })

    return render_template("index.html", labels=labels, temp_data=temp_data, rain_data=rain_data)


if __name__ == '__main__':
    app.run(debug=True)
