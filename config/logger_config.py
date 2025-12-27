import sys
from loguru import logger

def setup_logger(log_level="INFO"):
    """ロガーの初期設定を行う"""
    # 標準のロガー設定を削除
    logger.remove()

    # コンソール出力の設定（DEBUGを表示させない）
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        colorize=True
    )

    # ログファイルへの保存設定（トラブル調査用にDEBUGも全て残す）
    logger.add(
        "logs/app.log",
        rotation="10 MB",     # 10MBごとに新しいファイルにする
        retention="10 days",   # 10日分残す
        level="DEBUG",
        encoding="utf-8"
    )