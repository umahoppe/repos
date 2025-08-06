# データを整形・比較するスクリプト
import pandas as pd
import os


def load_and_aggregate(location, years):
    monthly_data = {}

    for year in years:
        filepath = f"data/raw/{location}/{year}.csv"
        if not os.path.exists(filepath):
            print(f"⚠️ ファイルが見つかりません: {filepath}")
            continue

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

    # 複数年を結合（横並びに）
    result = pd.concat(monthly_data.values(), axis=1)
    return result


if __name__ == "__main__":
    location = "Tokyo"
    years = [2021, 2022]

    print(f"📊 月別平均を計算中: {location}, {years}")
    df_result = load_and_aggregate(location, years)

    output_dir = f"data/processed/{location}"
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/monthly_comparison.csv"
    df_result.to_csv(output_path)

    print(f"✅ 整形データを保存しました: {output_path}")
    print(df_result)
