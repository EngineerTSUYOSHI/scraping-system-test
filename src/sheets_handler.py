import gspread
from google.oauth2.service_account import Credentials
from typing import List, Any
from loguru import logger
from config.settings import SPREADSHEET_ID, SERVICE_ACCOUNT_PATH, WORKSHEET_NAME


class GoogleSheetsHandler:
    """Googleスプレッドシートの読み書きを管理するクラス。

    認証、既存タイトルの取得、新規データの追記を担当する。
    """

    def __init__(self, spreadsheet_id: str = None, service_account_path: str = None):
        """初期化と認証を行う。

        :param spreadsheet_id: 対象スプレッドシートのID
        :param service_account_path: サービスアカウントのJSONファイルパス
        """
        self.spreadsheet_id: str = spreadsheet_id or SPREADSHEET_ID
        self.service_account_path: str = service_account_path or SERVICE_ACCOUNT_PATH
        self.worksheet_name: str = WORKSHEET_NAME
        self.scopes: List[str] = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        try:
            logger.info("GoogleSheetsHandler: 認証処理を開始します。")
            self.credentials = Credentials.from_service_account_file(
                service_account_path, scopes=self.scopes
            )
            self.gc = gspread.authorize(self.credentials)
            self.spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
            self.worksheet = self.spreadsheet.worksheet(self.worksheet_name)
            logger.info(
                f"GoogleSheetsHandler: '{self.worksheet_name}' に接続しました。"
            )
        except Exception as e:
            logger.error(f"GoogleSheetsHandler 初期化失敗: {e}")
            raise

    def get_existing_titles(self) -> List[str]:
        """現在スプレッドシートにあるタイトルをすべて取得する。

        :return: タイトルのリスト
        """
        logger.info("Method Start: get_existing_titles")
        try:
            # C1はヘッダーなので、C2以降を取得
            ROW_START = 3
            COLUMN_C = 2
            titles: List[str] = self.worksheet.col_values(COLUMN_C, ROW_START)

            logger.info(f"既存タイトルを {len(titles)} 件取得しました。")
            return titles
        except Exception as e:
            logger.error(f"タイトル取得中にエラーが発生しました: {e}")
            return []
        finally:
            logger.info("Method End: get_existing_titles")

    def add_new_jobs(self, job_rows: List[List[Any]]) -> bool:
        """B列を開始地点として、U列までの範囲にデータを書き込む。

        :param job_rows: 2次元リスト形式のデータ

        :return: 書き込み成功ならTrue、失敗ならFalse
        """
        if not job_rows:
            return False

        try:
            # C列のデータがある最終行を基準にする
            c_values = self.worksheet.col_values(3)
            next_row = len(c_values) + 1
            end_row = len(c_values) + len(job_rows)

            # 範囲を B列（取得日）〜 U列（URL）に固定
            # B列から数えて20列分 (B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U)
            target_range = f"B{next_row}:U{end_row}"

            logger.info(f"書き込み範囲: {target_range}")

            self.worksheet.update(
                target_range, job_rows, value_input_option="USER_ENTERED"
            )

            logger.success(f"{next_row}行目から{end_row}行目のB-U列に書き込み完了")
            return True

        except Exception as e:
            logger.error(f"データ追記失敗: {e}")
            return False
