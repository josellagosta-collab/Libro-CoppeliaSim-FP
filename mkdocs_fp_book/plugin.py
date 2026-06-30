from mkdocs.plugins import BasePlugin

from mkdocs_fp_book.database import KnowledgeBase
from mkdocs_fp_book.renderer import BookRenderer


class FPBookPlugin(BasePlugin):
    def on_config(self, config):
        self.kb = KnowledgeBase("knowledge")
        self.renderer = BookRenderer(self.kb)
        return config

    def on_page_markdown(self, markdown, page, config, files):
        return self.renderer.render(markdown, page)