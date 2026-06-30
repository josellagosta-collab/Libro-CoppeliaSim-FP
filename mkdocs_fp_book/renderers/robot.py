import re


class RobotRenderer:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def render(self, markdown, page):
        pattern = re.compile(
            r"::: robot\s*\n"
            r"id:\s*(.*?)\s*\n"
            r":::",
            re.DOTALL,
        )

        def replace(match):
            robot_id = match.group(1).strip()
            robot = self.kb.get_robot(robot_id)

            if robot is None:
                return f"""
<div class="fp-robot-card fp-robot-error">
  <strong>Robot no encontrado:</strong> {robot_id}
</div>
"""

            features = "\n".join(
                f"<li>{item}</li>" for item in robot.get("features", [])
            )
            used_in = ", ".join(robot.get("used_in", []))

            return f"""
<div class="fp-robot-card">
  <div class="fp-robot-title">🤖 {robot.get("name", robot_id)}</div>
  <div class="fp-robot-subtitle">{robot.get("type", "")}</div>

  <p>{robot.get("description", "")}</p>

  <table>
    <tr><th>Fabricante</th><td>{robot.get("manufacturer", "No indicado")}</td></tr>
    <tr><th>Usado en</th><td>{used_in}</td></tr>
  </table>

  <p><strong>Características principales:</strong></p>
  <ul>
    {features}
  </ul>

  <div class="fp-robot-note">
    <strong>Consejo para el profesor:</strong> {robot.get("teacher_note", "")}
  </div>
</div>
"""

        return pattern.sub(replace, markdown)