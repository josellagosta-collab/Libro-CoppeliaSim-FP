import re


class LearningRenderer:
    def render(self, markdown, page):
        markdown = self._render_objectives(markdown)
        markdown = self._render_summary(markdown)
        return markdown

    def _render_objectives(self, markdown):
        pattern = re.compile(
            r"::: objectives\s*\n"
            r"title:\s*(.*?)\s*\n"
            r"content:\s*\n\n"
            r"(.*?)\n:::",
            re.DOTALL,
        )

        def replace(match):
            title = match.group(1).strip()
            content = match.group(2).strip()

            return f"""
<div class="fp-objectives">
  <div class="fp-objectives-title">🎯 {title}</div>
  <div class="fp-objectives-content" markdown="1">

{content}

  </div>
</div>
"""

        return pattern.sub(replace, markdown)

    def _render_summary(self, markdown):
        pattern = re.compile(
            r"::: summary\s*\n"
            r"title:\s*(.*?)\s*\n"
            r"content:\s*\n\n"
            r"(.*?)\n:::",
            re.DOTALL,
        )

        def replace(match):
            title = match.group(1).strip()
            content = match.group(2).strip()

            return f"""
<div class="fp-summary">
  <div class="fp-summary-title">📌 {title}</div>
  <div class="fp-summary-content" markdown="1">

{content}

  </div>
</div>
"""

        return pattern.sub(replace, markdown)