import re


class CoverRenderer:
    def render(self, markdown, page):
        markdown = self._render_part_cover(markdown)
        markdown = self._render_chapter_cover(markdown)
        return markdown

    def _render_part_cover(self, markdown):
        pattern = re.compile(
            r"::: part-cover\s*\n"
            r"number:\s*(.*?)\s*\n"
            r"title:\s*(.*?)\s*\n"
            r"subtitle:\s*(.*?)\s*\n"
            r":::",
            re.DOTALL,
        )

        def replace(match):
            number = match.group(1).strip()
            title = match.group(2).strip()
            subtitle = match.group(3).strip()

            return f"""
<div class="fp-part-cover">
  <div class="fp-part-number">PARTE {number}</div>
  <div class="fp-part-title">{title}</div>
  <div class="fp-part-subtitle">{subtitle}</div>
</div>
"""

        return pattern.sub(replace, markdown)

    def _render_chapter_cover(self, markdown):
        pattern = re.compile(
            r"::: chapter-cover\s*\n"
            r"number:\s*(.*?)\s*\n"
            r"title:\s*(.*?)\s*\n"
            r"time:\s*(.*?)\s*\n"
            r"level:\s*(.*?)\s*\n"
            r":::",
            re.DOTALL,
        )

        def replace(match):
            number = match.group(1).strip()
            title = match.group(2).strip()
            time = match.group(3).strip()
            level = match.group(4).strip()

            return f"""
<div class="fp-chapter-cover">
  <div class="fp-chapter-number">CAPÍTULO {number}</div>
  <div class="fp-chapter-title">{title}</div>
  <div class="fp-chapter-meta">
    <span>⏱ Tiempo estimado: {time}</span>
    <span>🎓 Nivel: {level}</span>
  </div>
</div>
"""

        return pattern.sub(replace, markdown)