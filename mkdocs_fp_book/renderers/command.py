import re


class CommandRenderer:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def render(self, markdown, page):
        pattern = re.compile(
            r"::: command\s*\n"
            r"id:\s*(.*?)\s*\n"
            r":::",
            re.DOTALL,
        )

        def replace(match):
            command_id = match.group(1).strip()
            item = self.kb.get_coppeliasim_entry(command_id)

            if item is None:
                return f"""
<div class="fp-command-card fp-command-error">
  <strong>Comando no encontrado:</strong> {command_id}
</div>
"""

            errors = "\n".join(
                f"<li>{error}</li>" for error in item.get("common_errors", [])
            )

            used_in = ", ".join(item.get("used_in", []))

            return f"""
<div class="fp-command-card">
  <div class="fp-command-title">⚙️ {item.get("name", command_id)}</div>
  <div class="fp-command-subtitle">{item.get("type", "")}</div>

  <p>{item.get("description", "")}</p>

  <p><strong>Sintaxis:</strong></p>

```python
{item.get("syntax", "")}
<p><strong>Errores frecuentes:</strong></p> <ul> {errors} </ul> <p><strong>Usado en:</strong> {used_in}</p> <div class="fp-command-note"> <strong>Consejo para el profesor:</strong> {item.get("teacher_note", "")} </div> </div> """
        return pattern.sub(replace, markdown)