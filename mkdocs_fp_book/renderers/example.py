import re


class ExampleRenderer:
    """
    Renderiza bloques:

    ::: example
    caption: ...
    language: python
    content:

    print("Hola")
    :::
    """

    def render(self, markdown, page):
        chapter = self._chapter_number(page.file.src_path)
        counter = 0

        pattern = re.compile(
            r"::: example\s*\n"
            r"caption:\s*(.*?)\s*\n"
            r"language:\s*(.*?)\s*\n"
            r"content:\s*\n\n"
            r"(.*?)\n:::",
            re.DOTALL,
        )

        def replace(match):
            nonlocal counter
            counter += 1

            caption = match.group(1).strip()
            language = match.group(2).strip()
            content = match.group(3).rstrip()

            if chapter:
                number = f"{chapter}.{counter}"
            else:
                number = str(counter)

            return f"""
<div class="fp-example-caption">
    Ejemplo {number}. {caption}
</div>

```{language} linenums="1"
{content}
```
"""
        return pattern.sub(replace, markdown)

    def _chapter_number(self, path):
        match = re.search(r"capitulo(\d+)\.md", path)

        if match:
            return str(int(match.group(1)))

        return ""
