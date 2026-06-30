import re


class TableRenderer:
    def render(self, markdown, page):
        chapter = self._chapter_number(page.file.src_path)
        counter = 0

        pattern = re.compile(
            r"::: table\s*\n"
            r"caption:\s*(.*?)\s*\n"
            r"content:\s*\n\n"
            r"(.*?)\n:::",
            re.DOTALL,
        )

        def replace(match):
            nonlocal counter
            counter += 1

            caption = match.group(1).strip()
            content = match.group(2).strip()
            number = f"{chapter}.{counter}" if chapter else str(counter)

            return f"""
<div class="fp-table-caption">Tabla {number}. {caption}</div>

{content}
"""

        return pattern.sub(replace, markdown)

    def _chapter_number(self, path):
        match = re.search(r"capitulo(\d+)\.md", path)
        return str(int(match.group(1))) if match else ""