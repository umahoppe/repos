#!/bin/bash

# === 設定部分 ===
VENV_DIR="venv"
REQ_FILE="requirements.txt"

echo "=============================="
echo " Python 環境セットアップ開始 "
echo "=============================="

# 1. 仮想環境を削除
if [ -d "$VENV_DIR" ]; then
    echo "既存の仮想環境を削除中..."
    rm -rf "$VENV_DIR"
fi

# 2. 仮想環境を作成
echo "新しい仮想環境を作成中..."
python3 -m venv "$VENV_DIR"

# 3. 仮想環境を有効化
echo "仮想環境を有効化中..."
source "$VENV_DIR/bin/activate"

# 4. pip をアップグレード
echo "pip をアップグレード中..."
pip install --upgrade pip

# 5. requirements.txt からインストール
if [ -f "$REQ_FILE" ]; then
    echo "依存パッケージをインストール中..."
    pip install -r "$REQ_FILE"
else
    echo "requirements.txt が見つかりません。必要に応じて pip install を手動で実行してください。"
fi

echo "=============================="
echo " セットアップ完了！"
echo " 仮想環境を有効化するには:"
echo " source $VENV_DIR/bin/activate"
echo "=============================="