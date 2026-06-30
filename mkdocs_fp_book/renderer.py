from mkdocs_fp_book.renderers.figure import FigureRenderer
from mkdocs_fp_book.renderers.table import TableRenderer
from mkdocs_fp_book.renderers.example import ExampleRenderer
from mkdocs_fp_book.renderers.exercise import ExerciseRenderer
from mkdocs_fp_book.renderers.practice import PracticeRenderer
from mkdocs_fp_book.renderers.robot import RobotRenderer
from mkdocs_fp_book.renderers.python import PythonRenderer
from mkdocs_fp_book.renderers.sensor import SensorRenderer
from mkdocs_fp_book.renderers.command import CommandRenderer
from mkdocs_fp_book.renderers.glossary import GlossaryRenderer
from mkdocs_fp_book.renderers.cover import CoverRenderer
from mkdocs_fp_book.renderers.learning import LearningRenderer

class BookRenderer:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

        self.renderers = [
            CoverRenderer(),
            LearningRenderer(),
            FigureRenderer(),
            TableRenderer(),
            ExampleRenderer(),
            ExerciseRenderer(),
            PracticeRenderer(),
            RobotRenderer(self.kb),
            PythonRenderer(self.kb),
            SensorRenderer(self.kb),
            CommandRenderer(self.kb),
            GlossaryRenderer(self.kb),
        ]

    def render(self, markdown, page):
        for renderer in self.renderers:
            markdown = renderer.render(markdown, page)

        return markdown