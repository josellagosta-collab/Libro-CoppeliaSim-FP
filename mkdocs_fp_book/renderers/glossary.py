import re


class GlossaryRenderer:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def render(self, markdown, page):
        pattern = re.compile(
            r"::: glossary\s*\n"
            r"id:\s*(.*?)\s*\n"
            r":::",
            re.DOTALL,
        )

        def replace(match):
            entry_id = match.group(1).strip()
            item = self.kb.get_glossary_entry(entry_id)

            if item is None:
                return f"""
<div class="fp-glossary-card fp-glossary-error">
  <strong>Término no encontrado:</strong> {entry_id}
</div>
"""

            related = ", ".join(item.get("related", []))

            return f"""
<div class="fp-glossary-card">
  <div class="fp-glossary-title">📚 {item.get("term", entry_id)}</div>
  <div class="fp-glossary-subtitle">{item.get("category", "")}</div>

  <p>{item.get("definition", "")}</p>

  <p><strong>Relacionado con:</strong> {related}</p>

  <div class="fp-glossary-note">
    <strong>Consejo para el profesor:</strong> {item.get("teacher_note", "")}
  </div>
</div>
"""

        return pattern.sub(replace, markdown)