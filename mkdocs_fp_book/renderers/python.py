import re


class PythonRenderer:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def render(self, markdown, page):
        pattern = re.compile(
            r"::: python\s*\n"
            r"id:\s*(.*?)\s*\n"
            r":::",
            re.DOTALL,
        )

        def replace(match):
            function_id = match.group(1).strip()
            item = self.kb.get_python_function(function_id)

            if item is None:
                return f"""
<div class="fp-python-card fp-python-error">
  <strong>Funcion Python no encontrada:</strong> {function_id}
</div>
"""

            errors = "\n".join(
                f"<li>{error}</li>" for error in item.get("common_errors", [])
            )
            syntax = item.get("syntax", "").rstrip()
            example = item.get("example", "").rstrip()

            return f"""
<div class="fp-python-card">
  <div class="fp-python-title">Python: {item.get("name", function_id)}</div>

  <p>{item.get("description", "")}</p>

  <p><strong>Sintaxis:</strong></p>

```python
{syntax}
```

  <p><strong>Devuelve:</strong> {item.get("returns", "")}</p>

  <p><strong>Errores frecuentes:</strong></p>
  <ul>
    {errors}
  </ul>

  <p><strong>Ejemplo:</strong></p>

```python
{example}
```
</div>
"""

        return pattern.sub(replace, markdown)
