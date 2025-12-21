from datetime import datetime
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from loguru import logger


class Processor:
    """HTMLを解析し、データの抽出や判定を行うクラス"""

    def parse_list_to_datas(self, html: str) -> List[Dict[str, Any]]:
        """一覧ページのHTMLから案件情報の辞書リストを抽出する

        :param html: 一覧ページのHTMLテキスト

        :return: 案件情報の辞書リスト
        """
        soup = BeautifulSoup(html, "html.parser")
        job_datas = []

        # 案件カードの抽出
        job_cards = soup.select(".c-job-card.pc-show")

        for card in job_cards:
            title_el = card.select_one(".c-job-card__title")
            link_el = card.select_one(".c-job-card__heading a")

            if not title_el or not link_el:
                continue

            title = title_el.get_text(strip=True)
            full_url = link_el.get("href", "")

            # 単価の数値変換
            price_el = card.select_one(".c-job-price span")
            raw_price = 0
            if price_el:
                price_text = price_el.get_text(strip=True).replace(",", "")
                raw_price = int(price_text) if price_text.isdigit() else 0

            job_datas.append(
                {
                    "title": title,
                    "url": full_url,
                    "max_monthly": raw_price,
                    "get_date": datetime.now().strftime("%Y/%m/%d"),
                }
            )

        return job_datas

    def check_python_in_detail(self, html: str) -> bool:
        """詳細HTMLのJSON-LDからPythonが含まれるか判定する"""
        soup = BeautifulSoup(html, "html.parser")

        # すべてのJSON-LDを取得
        json_scripts = soup.find_all("script", type="application/ld+json")

        for script in json_scripts:
            # JobPostingが含まれるタグを探す
            if script.string and '"JobPosting"' in script.string:
                # 文字列検索で判定
                return "python" in script.string.lower()

        # JSON-LDが見つからない場合は全体テキストでフォールバック
        return "python" in soup.get_text().lower()

    def check_keywords_in_detail(self, html: str, keywords: List[str]) -> bool:
        """HTML中に指定されたキーワードのいずれかが含まれるか判定する。

        :param html: 詳細ページのHTML
        :param keywords: 検索したいワードのリスト (例: ["python", "django"])

        :return: キーワードのいずれかが含まれる、またはキーワードリストが空ならTrue
        """
        # 1. キーワードが空の場合は即時True
        if not keywords:
            return True

        soup = BeautifulSoup(html, "html.parser")

        # 2. 判定対象のテキストを探す (JobPostingのJSON-LD)
        target_json_str = ""
        json_scripts = soup.find_all("script", type="application/ld+json")
        for script in json_scripts:
            if script.string and '"JobPosting"' in script.string:
                target_json_str = script.string.lower()
                break

        # 詳細なテキストが見つからない場合はFalseを返す
        if not target_json_str:
            return False

        # 3. いずれかのキーワードが含まれているか判定
        # すべて小文字で比較するために、キーワードリストも小文字で回す
        for kw in keywords:
            if kw.lower() in target_json_str:
                logger.debug(f"キーワード検出: {kw}")
                return True

        return False
