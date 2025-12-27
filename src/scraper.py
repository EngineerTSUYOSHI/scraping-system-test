import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from loguru import logger

from config import settings


def get_session():
    """リトライ設定付きのセッションを取得する

    3回までリトライする。回数ごとに1秒ずつ待機時間を増やす。
    
    :return: requests.Session オブジェクト
    """
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504],
                  raise_on_status=False)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

class Scraper:
    """通信を担当し、生のHTML（テキスト）を取得するクラス"""

    def __init__(self):
        self.base_url = settings.SCRAPE_TARGET_URL
        self.headers = settings.HEADERS
        self.session = get_session()

    def fetch_list_page_html(self, page_num: int) -> str:
        """一覧ページのHTMLを取得する

        :param page_num: 取得するページ番号

        :return: 取得したHTMLのテキスト
        """
        url = f"{self.base_url}?page={page_num}"
        logger.info(f"ページ {page_num} を取得中: {url}")

        response = self.session.get(url, headers=self.headers, timeout=settings.TIMEOUT)
        response.raise_for_status()

        # サーバー負荷軽減
        time.sleep(settings.SLEEP_TIME)
        return response.text

    def fetch_detail_page_html(self, url: str) -> str:
        """詳細ページのHTMLを取得する

        :param url: 詳細ページのURL

        :return: 取得したHTMLのテキスト
        """
        logger.info(f"詳細ページ取得開始: {url}")
        response = requests.get(url, headers=self.headers, timeout=settings.TIMEOUT)
        response.raise_for_status()

        time.sleep(settings.SLEEP_TIME)
        return response.text
