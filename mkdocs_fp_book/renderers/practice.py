import re


class PracticeRenderer:
    def render(self, markdown, page):
        chapter = self._chapter_number(page.file.src_path)
        counter = 0

        pattern = re.compile(
            r"::: practice\s*\n"
            r"title:\s*(.*?)\s*\n"
            r"difficulty:\s*(.*?)\s*\n"
            r"time:\s*(.*?)\s*\n"
            r"content:\s*\n\n"
            r"(.*?)\n:::",
            re.DOTALL,
        )

        def replace(match):
            nonlocal counter
            counter += 1

            title = match.group(1).strip()
            difficulty = match.group(2).strip()
            time = match.group(3).strip()
            content = match.group(4).strip()
            number = f"{chapter}.{counter}" if chapter else str(counter)

            return f"""
<div class="fp-practice">
  <div class="fp-practice-title">Práctica {number}. {title}</div>
  <div class="fp-practice-meta">
    <span><strong>Dificultad:</strong> {difficulty}</span>
    <span><strong>Tiempo estimado:</strong> {time}</span>
  </div>
  <div class="fp-practice-content" markdown="1">

{content}

  </div>
</div>
"""

        return pattern.sub(replace, markdown)

    def _chapter_number(self, path):
        match = re.search(r"capitulo(\d+)\.md", path)
        return str(int(match.group(1))) if match else ""