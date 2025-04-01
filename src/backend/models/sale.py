from .base import BaseModel
from datetime import datetime

class Sale(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Convert date from string to datetime if needed
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, "%Y-%m-%d")

    def __repr__(self):
        return f"<Sale {self.date}: ${self.total} ({self.refunds} refunds)>"

    @classmethod
    def from_row(cls, row):
        return super().from_row(row)

# Optional: silence Pylance "unused import" warning
#_ = BaseModel
