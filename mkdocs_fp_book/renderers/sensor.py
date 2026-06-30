import re


class SensorRenderer:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def render(self, markdown, page):
        pattern = re.compile(
            r"::: sensor\s*\n"
            r"id:\s*(.*?)\s*\n"
            r":::",
            re.DOTALL,
        )

        def replace(match):
            sensor_id = match.group(1).strip()
            sensor = self.kb.get_sensor(sensor_id)

            if sensor is None:
                return f"""
<div class="fp-robot-card fp-robot-error">
  <strong>Sensor no encontrado:</strong> {sensor_id}
</div>
"""

            features = "\n".join(
                f"<li>{item}</li>" for item in sensor.get("features", [])
            )

            used_in = ", ".join(sensor.get("used_in", []))

            return f"""
<div class="fp-sensor-card">
  <div class="fp-sensor-title">📡 {sensor.get("name", sensor_id)}</div>
  <div class="fp-sensor-subtitle">{sensor.get("type", "")}</div>

  <p>{sensor.get("description", "")}</p>

  <p><strong>Características principales:</strong></p>
  <ul>
    {features}
  </ul>

  <p><strong>Usado en:</strong> {used_in}</p>

  <div class="fp-sensor-note">
    <strong>Consejo para el profesor:</strong> {sensor.get("teacher_note", "")}
  </div>
</div>
"""

        return pattern.sub(replace, markdown)