# src/models.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class JobEntity:
    title: str
    url: str
    max_monthly: int = 0
    get_date: Optional[str] = None
    is_target: bool = True

    @property
    def avg_monthly(self) -> int:
        if self.max_monthly == 0:
            return 0
        return (self.max_monthly + self.min_monthly) // 2
    @property
    def min_monthly(self) -> int:
        return self.max_monthly * 0.7
    
    @property
    def max_annual(self) -> int:
        return self.max_monthly * 12
    
    @property
    def min_annual(self) -> int:
        return self.min_monthly * 12

    def to_spreadsheet_row(self) -> list:
        """
        スプレッドシートのB列〜U列の構造に合わせてリストを生成する
        index(A列)はスプシ側で管理されている前提なので、B列から開始するデータを返す
        """
        # 引数で渡さなければ自動で取得日を入れる
        today = self.get_date or datetime.now().strftime("%Y/%m/%d")
        
        return [
            today,          # B: 取得日
            self.title,     # C: 案件名（タイトル）
            "",             # D: 雇用形態 (対象外)
            "",             # E: 地域 (対象外)
            "",             # F: 必要経験年数 (対象外)
            self.avg_monthly, # G: 月単価換算額
            self.min_annual,    # H: 最小年収
            self.max_annual,    # I: 最大年収
            self.min_monthly,   # J: 最小月収
            self.max_monthly,   # K: 最大月収
            "",             # L: 最小時給 (対象外)
            "",             # M: 最大時給 (対象外)
            "",             # N: AWS (対象外)
            "",             # O: Django (対象外)
            "",             # P: Flask (対象外)
            "",             # Q: Pandas (対象外)
            "",             # R: FastAPI (対象外)
            "",             # S: Docker (対象外)
            "",             # T: SQL (対象外)
            self.url        # U: URL
        ]