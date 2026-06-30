import re


class ExerciseRenderer:
    def render(self, markdown, page):
        chapter = self._chapter_number(page.file.src_path)
        counter = 0

        pattern = re.compile(
            r"::: exercise\s*\n"
            r"title:\s*(.*?)\s*\n"
            r"content:\s*\n\n"
            r"(.*?)\n:::",
            re.DOTALL,
        )

        def replace(match):
            nonlocal counter
            counter += 1

            title = match.group(1).strip()
            content = match.group(2).strip()
            number = f"{chapter}.{counter}" if chapter else str(counter)

            return f"""
<div class="fp-exercise">
  <div class="fp-exercise-title">Ejercicio {number}. {title}</div>
  <div class="fp-exercise-content" markdown="1">

{content}

  </div>
</div>
"""

        return pattern.sub(replace, markdown)

    def _chapter_number(self, path):
        match = re.search(r"capitulo(\d+)\.md", path)
        return str(int(match.group(1))) if match else ""