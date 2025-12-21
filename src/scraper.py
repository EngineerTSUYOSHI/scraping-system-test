import time

import requests
from loguru import logger

from config import settings


class Scraper:
    """通信を担当し、生のHTML（テキスト）を取得するクラス"""

    def __init__(self):
        self.base_url = settings.SCRAPE_TARGET_URL
        self.headers = settings.HEADERS

    def fetch_list_page_html(self, page_num: int) -> str:
        """一覧ページのHTMLを取得する

        :param page_num: 取得するページ番号

        :return: 取得したHTMLのテキスト
        """
        url = f"{self.base_url}?page={page_num}"
        logger.debug(f"ページ {page_num} を取得中: {url}")

        response = requests.get(url, headers=self.headers, timeout=settings.TIMEOUT)
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
