import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# プロジェクトのルートディレクトリを取得
BASE_DIR = Path(__file__).resolve().parent.parent

# Google API 設定
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "your-spreadsheet-id-here")
SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH", str(BASE_DIR / "service_account.json"))

# シート設定
WORKSHEET_NAME = "Python別、案件ランキング"

# スクレイピング設定
SCRAPE_TARGET_URL = "https://itpropartners.com/job/engineer/python"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
START_PAGE = 1
MAX_PAGES_TO_SCRAPE = 10  # 1から10ページまでスクレイピングするための設定
TIMEOUT = 15  # タイムアウト時間（秒）
SLEEP_TIME = 1  # 秒

# 検索キーワードリスト
KEYWORDS = [
    "python",
]
