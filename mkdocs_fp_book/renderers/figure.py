import posixpath
import re
from pathlib import Path


class FigureRenderer:
    def render(self, markdown, page):
        chapter = self._chapter_number(page.file.src_path)
        counter = 0

        pattern = re.compile(
            r"::: figure\s*\n"
            r"image:\s*(.*?)\s*\n"
            r"caption:\s*(.*?)\s*\n"
            r":::",
            re.DOTALL,
        )

        def replace(match):
            nonlocal counter
            counter += 1

            image = match.group(1).strip()
            caption = match.group(2).strip()
            image_url = self._make_relative_url(image, page.file.src_path)
            number = f"{chapter}.{counter}" if chapter else str(counter)

            return f"""
<div class="figure">
  <img src="{image_url}" alt="{caption}">
  <div class="figure-caption">Figura {number}. {caption}</div>
</div>
"""

        return pattern.sub(replace, markdown)

    def _chapter_number(self, path):
        match = re.search(r"capitulo(\d+)\.md", path)
        return str(int(match.group(1))) if match else ""

    def _make_relative_url(self, image_path, page_src_path):
        source_dir = posixpath.dirname(page_src_path)
        target_source_path = posixpath.normpath(posixpath.join(source_dir, image_path))

        page_path = Path(page_src_path)

        if page_path.name == "index.md":
            output_dir = posixpath.dirname(page_src_path)
        else:
            output_dir = posixpath.join(posixpath.dirname(page_src_path), page_path.stem)

        depth = len([part for part in output_dir.split("/") if part])
        return "../" * depth + target_source_path