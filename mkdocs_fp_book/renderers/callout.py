import re
import textwrap


class CalloutRenderer:
    def render(self, markdown, page):
        markdown = self._render_simple_block(
            markdown,
            block_name="teacher",
            admonition_type="teacher",
            icon="👨‍🏫",
            default_title="Consejo para el profesor",
        )

        markdown = self._render_simple_block(
            markdown,
            block_name="common-error",
            admonition_type="common-error",
            icon="⚠️",
            default_title="Error frecuente",
        )

        markdown = self._render_simple_block(
            markdown,
            block_name="challenge",
            admonition_type="challenge",
            icon="🚀",
            default_title="Reto",
        )

        return markdown

    def _render_simple_block(self, markdown, block_name, admonition_type, icon, default_title):
        pattern = re.compile(
            rf"::: {block_name}\s*\n"
            r"(.*?)\n:::",
            re.DOTALL,
        )

        def replace(match):
            raw_content = match.group(1).strip()
            title = default_title
            content = raw_content

            lines = raw_content.splitlines()

            if lines and lines[0].startswith("title:"):
                title = lines[0].replace("title:", "", 1).strip()
                content = "\n".join(lines[1:]).strip()

            if content.startswith("content:"):
                content = content.replace("content:", "", 1).strip()

            indented_content = textwrap.indent(content, "    ")

            return f'''
!!! {admonition_type} "{icon} {title}"

{indented_content}
'''

        return pattern.sub(replace, markdown)