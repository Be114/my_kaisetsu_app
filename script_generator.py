from openai import OpenAI
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    print("エラー: OPENROUTER_API_KEYが .env ファイルに設定されていません。")
    exit()

# OpenRouterクライアントの初期化
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
)

# 使用するモデルを選択 (OpenRouterで提供されているモデル名)
# 例: "google/gemini-1.5-flash-latest", "google/gemini-pro", "mistralai/mistral-7b-instruct" など
# ユーザーが提示した "google/gemini-2.5-pro-preview" が利用可能か確認してください。
# ここでは例として "google/gemini-1.5-flash-latest" を使用します。
MODEL_NAME = "google/gemini-2.5-pro-preview" # ★ご自身で利用したいモデル名に変更してください

def generate_script_via_openrouter(input_text_content, title=""):
    """
    入力テキストから解説とセリフ形式の台本をOpenRouter経由で生成する関数
    """
    if not title:
        title = input_text_content[:30] + "..."

    # プロンプトは前回と同様
    prompt = f"""
    以下のテキストの内容について、簡潔な解説と、その内容を分かりやすく伝えるためのAとBのキャラクターによる掛け合いセリフを作成してください。

    ## 入力テキスト
    {input_text_content}

    ## 指示
    1. まず、入力テキスト全体の要点をまとめた「### 解説」を作成してください。解説は300字以内を目安とします。
    2. 次に、その解説内容を補足したり、面白おかしく伝えたりする「### セリフ」をAとBの2人のキャラクターで作成してください。
       - Aは聞き手、Bは説明役のようなキャラクターを想定してください。
       - セリフは5往復以上で、各セリフは簡潔にしてください。
       - 各セリフの前に「A: 」や「B: 」のように話者を示してください。
    3. 全体として、親しみやすく、分かりやすい言葉遣いを心がけてください。
    4. マークダウン形式で出力してください。
    """

    try:
        print(f"モデル '{MODEL_NAME}' を使用してOpenRouterにリクエストを送信します...")
        completion = client.chat.completions.create(
            # extra_headers は削除
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )
        generated_text = completion.choices[0].message.content
        return generated_text
    except Exception as e:
        print(f"OpenRouter APIとの通信中にエラーが発生しました: {e}")
        if hasattr(e, 'response') and e.response:
            try:
                print(f"API Response: {e.response.json()}")
            except: # pylint: disable=bare-except
                print(f"API Response (raw): {e.response.text}")
        return None

if __name__ == "__main__":
    input_file_path = "input.txt" # スクリプトと同じディレクトリを想定
    # my_kaisetsu_app ディレクトリ内の input.txt を参照するように修正
    # ただし、ユーザーの指示では「スクリプトと同じディレクトリに input.txt」とあるため、
    # スクリプト実行時のカレントディレクトリが my_kaisetsu_app であることを前提とします。
    # もしそうでなければ、os.path.join(os.path.dirname(__file__), "input.txt") のような指定が必要です。

    try:
        with open(input_file_path, "r", encoding="utf-8") as f:
            text_content = f.read()
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_file_path}' が見つかりません。スクリプトと同じディレクトリに配置してください。")
        exit()

    print("台本を生成中です (OpenRouter経由)...")
    generated_script_text = generate_script_via_openrouter(text_content, title="私の最初の解説")

    if generated_script_text:
        output_script_file = "generated_script_openrouter.md" # スクリプトと同じディレクトリを想定
        with open(output_script_file, "w", encoding="utf-8") as f:
            f.write(generated_script_text)
        print(f"台本が '{output_script_file}' に保存されました。")
        print("\n--- 生成された台本 (OpenRouter) ---")
        print(generated_script_text)
        print("----------------------------------\n")
    else:
        print("台本の生成に失敗しました。")