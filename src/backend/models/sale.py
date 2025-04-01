from datetime import datetime

class Sale:
    def __init__(self, id, date, total, refunds):
        self.id = id
        self.date = date
        self.total = total
        self.refunds = refunds

    @classmethod
    def from_row(cls, row):
        parsed_date = datetime.strptime(row["date"], "%Y-%m-%d")
        return cls(
            id=row["id"],
            date=parsed_date,
            total=row["total"],
            refunds=row["refunds"]
        )

    def __repr__(self):
        return f"<Sale {self.date}: ${self.total} ({self.refunds} refunds)>"
