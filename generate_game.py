import os
from groq import Groq

# Groqクライアントの初期化
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=api_key)

# 開発対象のゲームファイルパス (今回は1つのゲームを徹底的に育てるため、直下の index.html を対象にします)
file_path = "index.html"

# すでにゲームが存在するかチェック
if os.path.exists(file_path):
    # 既存のコードを読み込む
    with open(file_path, "r", encoding="utf-8") as f:
        current_code = f.read()
    
    print("Found existing game. Preparing to improve it...")
    
    # 改善用のプロンプト
    prompt = f"""
あなたは世界的なインディーゲーム開発者です。
目標は、itch.ioで有料販売（数ドル）してもプレイヤーが満足するクオリティのブラウザゲームを作ることです。

以下は、現在開発中のゲーム（HTML/CSS/JSの一体型コード）です。
このゲームを分析し、**ゲーム性、ビジュアル（CSSグラフィック、Canvas、アニメーション）、サウンド（Web Audio APIによるBGMや効果音）、あるいは新しいゲーム要素（アップグレードシステム、ステージ、スコア保存、敵の種類など）の追加**を行い、ゲームのクオリティを一段階上げてください。

【改善のルール】
- 変更や機能追加は1回につき1〜2個に絞り、確実に動作するようにしてください。
- 外部のアセット（画像や音楽ファイルなど）は使えません。グラフィックはCSSやHTML5 Canvas、音楽・効果音はWeb Audio APIを使ってシンセサイズ（自動生成）してください。
- 外部ライブラリ（Phaser.jsやThree.jsなど）は読み込まず、ピュアなHTML/CSS/JavaScript（Vanilla JS）で書いてください。
- 説明やマークダウン記法(```html)は絶対に含めず、<!DOCTYPE html> から始まるHTMLコード全体のみをプレーンテキストで出力してください。

【現在のコード】
{current_code}
"""
else:
    print("No existing game found. Creating a new game from scratch...")
    
    # 新規作成用のプロンプト
    prompt = """
あなたは世界的なインディーゲーム開発者です。
目標は、itch.ioで有料販売できるクオリティのブラウザゲームを作ることです。

完全に動作する、面白くて美しく、思わずハマってしまうユニークなブラウザゲーム（HTML5/CSS/JavaScript）を1ファイル（index.html）で作成してください。

【ルールの詳細】
- 外部アセット（画像や音楽ファイル）は使用せず、CSS、HTML5 Canvas、絵文字などで極めて美しいビジュアルを作成してください。
- 音楽や効果音は、Web Audio API（JavaScript）を使ってシンセサイズして実装してください（ミュート機能も付けること）。
- 外部ライブラリは読み込まず、バニラJavaScriptで実装してください。
- 説明やマークダウン記法(```html)は絶対に含めず、<!DOCTYPE html> から始まるHTMLコード全体のみをプレーンテキストで出力してください。
"""

# Groq API呼び出し
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.6,  # 安定して動くコードを出力するため少し低めに設定
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

# 保存（上書き）
with open(file_path, "w", encoding="utf-8") as f:
    f.write(game_code)

print(f"Successfully updated/created the game at {file_path} using Llama-3.3!")
