# 解説台本ジェネレータ

## 概要

このスクリプトは、入力されたテキストに基づいて、AIモデル（OpenRouter経由）を使用し、簡潔な解説とその内容を分かりやすく伝えるためのキャラクターによる掛け合い形式の台本を自動生成します。

## 主な機能

-   `input.txt`（または設定ファイルで指定されたパス）から原文を読み込みます。
-   OpenRouter APIを利用してAIモデルにリクエストを送信し、解説と台本を生成します。
-   生成された内容は `generated_script_openrouter.md`（または設定ファイルで指定されたパス）に保存されます。

## 要件

-   Python 3.7 以降
-   `openai` ライブラリ
-   `python-dotenv` ライブラリ

## セットアップ手順

1.  **リポジトリのクローン**:
    ```bash
    git clone https://github.com/user/your-repo-name.git
    cd your-repo-name
    ```

2.  **依存関係のインストール**:
    ```bash
    pip install openai python-dotenv
    ```

3.  **.env ファイルの作成**:
    リポジトリのルートディレクトリに `.env` という名前のファイルを作成してください。

4.  **APIキーの設定**:
    作成した `.env` ファイルに、ご自身のOpenRouter APIキーを以下のように記述します:
    ```env
    OPENROUTER_API_KEY="your_actual_api_key_here"
    ```
    `your_actual_api_key_here` の部分を実際のAPIキーに置き換えてください。

## 設定 (`config.py`)

スクリプトの動作は `config.py` ファイルを通じて設定可能です。

-   `MODEL_NAME`: 使用するAIモデルの名前。OpenRouterで利用可能なモデル名を指定してください。(例: `"google/gemini-1.5-flash-latest"`, `"mistralai/mistral-7b-instruct"`)
-   `INPUT_FILE_PATH`: 入力テキストファイルのパス。(デフォルト: `"input.txt"`)
-   `OUTPUT_SCRIPT_FILE`: 生成された台本を保存するファイルのパス。(デフォルト: `"generated_script_openrouter.md"`)
-   `DEFAULT_TITLE_PREFIX`: 台本生成時に使用されるデフォルトのタイトル。(デフォルト: `"私の最初の解説"`)

必要に応じてこれらの値を変更してください。

## 使用方法

1.  **入力テキストの準備**:
    `input.txt` ファイル（または `config.py` で `INPUT_FILE_PATH` に指定したファイル）に、台本の元となるテキストを記述します。

2.  **スクリプトの実行**:
    ターミナルで以下のコマンドを実行します:
    ```bash
    python script_generator.py
    ```

3.  **出力の確認**:
    スクリプトの実行が完了すると、`generated_script_openrouter.md` ファイル（または `config.py` で `OUTPUT_SCRIPT_FILE` に指定したファイル）に生成された台本が出力されます。ログはコンソールにも表示されます。
