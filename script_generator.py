from openai import OpenAI, APIError
import os
from dotenv import load_dotenv
import config
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# .envファイルから環境変数を読み込む
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    logging.error("OPENROUTER_API_KEYが .env ファイルに設定されていません。")
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
MODEL_NAME = config.MODEL_NAME # ★ご自身で利用したいモデル名に変更してください

def read_input_file(file_path: str) -> str:
    """
    指定されたファイルパスからテキストコンテンツを読み込む関数
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"入力ファイル '{file_path}' が見つかりません。スクリプトと同じディレクトリに配置してください。")
        exit()
    except IOError as e:
        logging.error(f"ファイル '{file_path}' の読み込み中にIOErrorが発生しました: {e}")
        exit()

def write_output_file(file_path: str, content: str):
    """
    指定されたファイルパスにコンテンツを書き込む関数
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"台本が '{file_path}' に保存されました。")
    except IOError as e:
        logging.error(f"ファイル '{file_path}' への書き込み中にIOErrorが発生しました: {e}")

def generate_script_via_openrouter(input_text_content: str, title: str):
    """
    入力テキストから解説とセリフ形式の台本をOpenRouter経由で生成する関数
    """
    # title引数は呼び出し元で設定されるため、ここでのデフォルト設定は不要

    # プロンプトは前回と同様
    # title 変数をプロンプト内で使用する場合は、呼び出し側で適切に設定されていることを確認
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
        logging.info(f"モデル '{config.MODEL_NAME}' を使用してOpenRouterにリクエストを送信します...")
        completion = client.chat.completions.create(
            # extra_headers は削除
            model=config.MODEL_NAME, # Ensure this uses config.MODEL_NAME if MODEL_NAME global isn't already that.
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )
        generated_text = completion.choices[0].message.content
        return generated_text
    except APIError as e:
        logging.error(f"OpenRouter APIリクエスト中にエラーが発生しました (モデル: {config.MODEL_NAME}): {e}")
        if hasattr(e, 'response') and e.response:
            try:
                logging.error(f"API Response: {e.response.json()}")
            except: # pylint: disable=bare-except
                logging.error(f"API Response (raw): {e.response.text}")
        return None
    except Exception as e:
        logging.error(f"OpenRouter APIとの通信中に予期せぬエラーが発生しました: {e}")
        # Potentially, e.response might not exist for non-APIError exceptions
        # Depending on the nature of 'e', you might not always have 'e.response'
        # Consider a more generic error logging here if needed.
        return None

def main():
    """
    スクリプトのメイン処理をオーケストレーションする関数
    """
    # 入力ファイルの読み込み
    # my_kaisetsu_app ディレクトリ内の input.txt を参照するように修正
    # ただし、ユーザーの指示では「スクリプトと同じディレクトリに input.txt」とあるため、
    # スクリプト実行時のカレントディレクトリが my_kaisetsu_app であることを前提とします。
    # もしそうでなければ、os.path.join(os.path.dirname(__file__), config.INPUT_FILE_PATH) のような指定が必要です。
    text_content = read_input_file(config.INPUT_FILE_PATH)

    logging.info("台本を生成中です (OpenRouter経由)...")
    # generate_script_via_openrouter に config.DEFAULT_TITLE_PREFIX を渡す
    generated_script_text = generate_script_via_openrouter(text_content, title=config.DEFAULT_TITLE_PREFIX)

    if generated_script_text:
        # write_output_file now logs success internally, so no need to log here explicitly for that part
        # The instruction "Replace print(f"台本が '{config.OUTPUT_SCRIPT_FILE}' に保存されました。")" is handled inside write_output_file
        logging.info("\n--- 生成された台本 (OpenRouter) ---")
        logging.info(f"生成された台本:\n{generated_script_text}")
        logging.info("----------------------------------\n")
    else:
        logging.error("台本の生成に失敗しました。")

if __name__ == "__main__":
    main()