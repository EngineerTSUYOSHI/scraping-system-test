import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from loguru import logger

from config import settings
from src.models import JobEntity
from src.processor import Processor
from src.scraper import Scraper
from src.sheets_handler import GoogleSheetsHandler


def main():
    handler = GoogleSheetsHandler()
    scraper = Scraper()
    processor = Processor()

    # スプレッドシートから既存タイトルを取得
    existing_titles = handler.get_existing_titles()

    # 対象サイトからスクレイピング結果を取得
    job_datas = []
    for p in range(settings.START_PAGE, settings.MAX_PAGES_TO_SCRAPE + 1):
        try:
            html = scraper.fetch_list_page_html(p)
            job_datas.extend(processor.parse_list_to_datas(html))
        except Exception as e:
            logger.error(f"一覧ページ {p} の取得に失敗しました: {e}")
            continue

    # 取得したデータのタイトルが既存タイトルに含まれていなければJobEntityを作成
    jobs = []
    for job_data in job_datas:
        if job_data["title"] in existing_titles:
            continue
        job = JobEntity(
            title=job_data["title"],
            url=job_data["url"],
            max_monthly=job_data["max_monthly"],
            get_date=job_data["get_date"],
        )
        jobs.append(job)

    # 詳細ページのHTMLを取得し、検索対象文字が含まれるかをチェック
    for job in jobs:
        try:
            detail_html = scraper.fetch_detail_page_html(job.url)
            is_target = processor.check_keywords_in_detail(
                detail_html, settings.KEYWORDS
            )
            # 検索対象文字が含まれるかの判定結果をセット
            job.is_target = is_target
        except Exception as e:
            logger.warning(
                f"詳細ページの解析に失敗したためスキップします ({job.url}): {e}"
            )
            job.is_target = False

    # JobEntityからスプレッドシート用の行データに変換して追加処理実行
    jobs_list = [job.to_spreadsheet_row() for job in jobs if job.is_target]

    if jobs_list:
        handler.add_new_jobs(jobs_list)
        logger.success(
            f"{len(jobs_list)} 件の新規案件をスプレッドシートに追加しました。"
        )
    else:
        logger.info("追加対象の新規案件はありませんでした。")


if __name__ == "__main__":
    main()
