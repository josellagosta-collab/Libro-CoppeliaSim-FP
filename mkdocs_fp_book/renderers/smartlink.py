import re
from html import escape


class SmartLinkRenderer:
    """
    Convierte referencias cortas [[id]] en fichas automáticas.

    Busca el id en este orden:

    1. Robots
    2. Sensores
    3. Funciones Python
    4. Comandos CoppeliaSim
    5. Glosario
    """

    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def render(self, markdown, page):
        pattern = re.compile(r"\[\[([A-Za-z0-9_\-\.]+)\]\]")

        def replace(match):
            item_id = match.group(1).strip()

            robot = self.kb.get_robot(item_id)
            if robot is not None:
                return self._robot_card(item_id, robot)

            sensor = self.kb.get_sensor(item_id)
            if sensor is not None:
                return self._sensor_card(item_id, sensor)

            python_function = self.kb.get_python_function(item_id)
            if python_function is not None:
                return self._python_card(item_id, python_function)

            command = self.kb.get_coppeliasim_entry(item_id)
            if command is not None:
                return self._command_card(item_id, command)

            glossary = self.kb.get_glossary_entry(item_id)
            if glossary is not None:
                return self._glossary_card(item_id, glossary)

            return f"`[[{escape(item_id)}]]`"

        return pattern.sub(replace, markdown)

    def _robot_card(self, item_id, item):
        features = "\n".join(
            f"<li>{escape(str(feature))}</li>" for feature in item.get("features", [])
        )
        used_in = ", ".join(str(value) for value in item.get("used_in", []))

        return f"""
<div class="fp-robot-card">
  <div class="fp-robot-title">🤖 {escape(str(item.get('name', item_id)))}</div>
  <div class="fp-robot-subtitle">{escape(str(item.get('type', '')))}</div>
  <p>{escape(str(item.get('description', '')))}</p>
  <p><strong>Usado en:</strong> {escape(used_in)}</p>
  <p><strong>Características principales:</strong></p>
  <ul>
    {features}
  </ul>
</div>
"""

    def _sensor_card(self, item_id, item):
        features = "\n".join(
            f"<li>{escape(str(feature))}</li>" for feature in item.get("features", [])
        )
        used_in = ", ".join(str(value) for value in item.get("used_in", []))

        return f"""
<div class="fp-sensor-card">
  <div class="fp-sensor-title">📡 {escape(str(item.get('name', item_id)))}</div>
  <div class="fp-sensor-subtitle">{escape(str(item.get('type', '')))}</div>
  <p>{escape(str(item.get('description', '')))}</p>
  <p><strong>Usado en:</strong> {escape(used_in)}</p>
  <ul>
    {features}
  </ul>
</div>
"""

    def _python_card(self, item_id, item):
        errors = "\n".join(
            f"<li>{escape(str(error))}</li>" for error in item.get("common_errors", [])
        )
        syntax = escape(str(item.get("syntax", "")))
        example = escape(str(item.get("example", "")))

        return f"""
<div class="fp-python-card">
  <div class="fp-python-title">🐍 {escape(str(item.get('name', item_id)))}</div>
  <p>{escape(str(item.get('description', '')))}</p>
  <p><strong>Sintaxis:</strong></p>
  <pre><code class="language-python">{syntax}</code></pre>
  <p><strong>Devuelve:</strong> {escape(str(item.get('returns', '')))}</p>
  <p><strong>Errores frecuentes:</strong></p>
  <ul>{errors}</ul>
  <p><strong>Ejemplo:</strong></p>
  <pre><code>{example}</code></pre>
</div>
"""

    def _command_card(self, item_id, item):
        errors = "\n".join(
            f"<li>{escape(str(error))}</li>" for error in item.get("common_errors", [])
        )
        used_in = ", ".join(str(value) for value in item.get("used_in", []))
        syntax = escape(str(item.get("syntax", "")))

        return f"""
<div class="fp-command-card">
  <div class="fp-command-title">⚙️ {escape(str(item.get('name', item_id)))}</div>
  <div class="fp-command-subtitle">{escape(str(item.get('type', '')))}</div>
  <p>{escape(str(item.get('description', '')))}</p>
  <p><strong>Sintaxis:</strong></p>
  <pre><code>{syntax}</code></pre>
  <p><strong>Usado en:</strong> {escape(used_in)}</p>
  <p><strong>Errores frecuentes:</strong></p>
  <ul>{errors}</ul>
</div>
"""

    def _glossary_card(self, item_id, item):
        related = ", ".join(str(value) for value in item.get("related", []))

        return f"""
<div class="fp-glossary-card">
  <div class="fp-glossary-title">📚 {escape(str(item.get('term', item_id)))}</div>
  <div class="fp-glossary-subtitle">{escape(str(item.get('category', '')))}</div>
  <p>{escape(str(item.get('definition', '')))}</p>
  <p><strong>Relacionado con:</strong> {escape(related)}</p>
</div>
"""