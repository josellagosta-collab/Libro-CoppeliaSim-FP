from mkdocs_fp_book.renderers.figure import FigureRenderer
from mkdocs_fp_book.renderers.table import TableRenderer
from mkdocs_fp_book.renderers.example import ExampleRenderer
from mkdocs_fp_book.renderers.exercise import ExerciseRenderer


class BookRenderer:

    def __init__(self, knowledge_base):
        self.kb = knowledge_base

        self.renderers = [
            FigureRenderer(),
            TableRenderer(),
            ExampleRenderer(),
            ExerciseRenderer(),
        ]

    def render(self, markdown, page):
        for renderer in self.renderers:
            markdown = renderer.render(markdown, page)

        return markdown