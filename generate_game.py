import os
import datetime
from groq import Groq

# Groqクライアントの初期化
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=api_key)

# 今週の週番号を取得 (例: week-2026-28)
week_str = datetime.datetime.now().strftime("week-%Y-%U")

# AIにゲームの生成を依頼するプロンプト
prompt = """
あなたは天才ゲームクリエイターです。
完全に動作する、面白くてユニークなブラウザゲーム（HTML5/CSS/JavaScript）を1ファイル（index.html）で作成してください。
外部のアセット（画像や外部のJSライブラリ）は使わず、CSSのグラフィックやCanvas、絵文字等で表現してください。
HTMLコードのみをプレーンテキストで出力してください（マークダウンの ```html や説明テキストは絶対に含めず、<!DOCTYPE html> から書き始めてください）。
"""

print(f"Requesting game generation using llama-3.3-70b-versatile...")

# GroqのAPIを呼び出し (Llama 3.3 70B モデルを使用)
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=8192,
)

# レスポンスからテキストを抽出
game_code = completion.choices[0].message.content.strip()

# クレンジング処理
if game_code.startswith("```html"):
    game_code = game_code[7:]
elif game_code.startswith("```"):
    game_code = game_code[3:]

if game_code.endswith("```"):
    game_code = game_code[:-3]

game_code = game_code.strip()

# フォルダを作って保存
os.makedirs(week_str, exist_ok=True)
file_path = f"{week_str}/index.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(game_code)

print(f"Successfully generated game at {file_path}")
