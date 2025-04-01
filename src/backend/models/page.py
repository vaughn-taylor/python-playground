import markdown
from .base import BaseModel

class Page(BaseModel):
    def render_content(self):
        return markdown.markdown(self.content, extensions=["extra", "smarty"])
