import os

# プロジェクトのルートディレクトリ名
project_name = "agri-weather-compare"

# 作成するディレクトリとサブディレクトリの構成
folders = [
    "app/templates",
    "app/static/css",
    "app/static/js",
    "app/static/images",
    "data/raw",
    "data/processed",
    "scripts",
    "notebooks",
    "tests"
]

# 作成する初期ファイルとその中身（必要最低限）
files = {
    "README.md": "# Agri Weather Compare\n\n農業の作付け計画に役立つ過去気象データ比較ツール。",
    ".gitignore": "__pycache__/\n.env\n*.pyc\ndata/\n",
    "requirements.txt": "# 必要なPythonパッケージをここに記述\nflask\npandas\n",
    "app/__init__.py": "# Flask初期化コードをここに記述予定\n",
    "app/routes.py": "# ルーティングをここに記述\n",
    "app/templates/index.html": "<!-- HTMLテンプレートのトップページ -->\n<html><body><h1>Agri Weather Compare</h1></body></html>",
    "scripts/fetch_data.py": "# 気象データを取得するスクリプト\n",
    "scripts/process_data.py": "# データを整形・比較するスクリプト\n",
    "notebooks/analysis_sample.ipynb": "",  # 空でOK
    "tests/test_routes.py": "# ルーティングのテストコード\n",
    "config.py": "# 設定情報（APIキーなど）をここに記述\n"
}

# ディレクトリ作成
os.makedirs(project_name, exist_ok=True)
for folder in folders:
    os.makedirs(os.path.join(project_name, folder), exist_ok=True)

# ファイル作成
for path, content in files.items():
    full_path = os.path.join(project_name, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"✅ プロジェクト構成が作成されました：{project_name}/")
