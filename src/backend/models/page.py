
from .base import BaseModel

class Page(BaseModel):
    def __repr__(self):
        return f"<Page {self.slug}: {self.title}>"
