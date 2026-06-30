import posixpath
import re
from pathlib import Path

import yaml
from mkdocs.plugins import BasePlugin
from mkdocs_fp_book.database import KnowledgeBase


class FPBookPlugin(BasePlugin):
    """
    Plugin editorial para libros técnicos de FP con MkDocs.

    Bloques soportados:

    ::: figure
    image: ../assets/logos/logo.svg
    caption: Texto de la figura
    :::

    ::: table
    caption: Texto de la tabla
    content:

    | A | B |
    |---|---|
    | 1 | 2 |
    :::

    ::: example
    caption: Texto del ejemplo
    language: python
    content:

    print("Hola")
    :::

    ::: exercise
    title: Título del ejercicio
    content:

    Texto del ejercicio.
    :::

    ::: practice
    title: Título de la práctica
    difficulty: Baja
    time: 20 minutos
    content:

    Pasos de la práctica.
    :::

    ::: robot
    id: PioneerP3DX
    :::
    """

    def on_page_markdown(self, markdown, page, config, files):
        chapter = self._chapter_number(page.file.src_path)

        markdown = self._process_figures(markdown, page, chapter)
        markdown = self._process_tables(markdown, chapter)
        markdown = self._process_examples(markdown, chapter)
        markdown = self._process_exercises(markdown, chapter)
        markdown = self._process_practices(markdown, chapter)
        markdown = self._process_robots(markdown)
        markdown = self._process_robots(markdown)

        return markdown

    # ---------------------------------------------------------
    # FIGURAS
    # ---------------------------------------------------------

    def _process_figures(self, markdown, page, chapter):
        counter = 0

        pattern = re.compile(
            r"::: figure\s*\n"
            r"image:\s*(.*?)\s*\n"
            r"caption:\s*(.*?)\s*\n"
            r":::",
            re.DOTALL,
        )

        def replace(match):
            nonlocal counter
            counter += 1

            image = match.group(1).strip()
            caption = match.group(2).strip()
            image_url = self._make_relative_url(image, page.file.src_path)
            number = self._number(chapter, counter)

            return f"""
<div class="figure">
  <img src="{image_url}" alt="{caption}">
  <div class="figure-caption">Figura {number}. {caption}</div>
</div>
"""

        return pattern.sub(replace, markdown)

    # ---------------------------------------------------------
    # TABLAS
    # ---------------------------------------------------------

    def _process_tables(self, markdown, chapter):
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
            number = self._number(chapter, counter)

            return f"""
<div class="fp-table-caption">Tabla {number}. {caption}</div>

{content}
"""

        return pattern.sub(replace, markdown)

    # ---------------------------------------------------------
    # EJEMPLOS DE CÓDIGO
    # ---------------------------------------------------------

    def _process_examples(self, markdown, chapter):
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
            number = self._number(chapter, counter)

            return f"""<div class="fp-example-caption">Ejemplo {number}. {caption}</div>

```{language} linenums="1"
{content}
```
"""

        return pattern.sub(replace, markdown)

    # ---------------------------------------------------------
    # EJERCICIOS
    # ---------------------------------------------------------

    def _process_exercises(self, markdown, chapter):
        counter = 0

        pattern = re.compile(
            r"::: exercise\s*\n"
            r"title:\s*(.*?)\s*\n"
            r"content:\s*\n\n"
            r"(.*?)\n:::",
            re.DOTALL,
        )

        def replace(match):
            nonlocal counter
            counter += 1

            title = match.group(1).strip()
            content = match.group(2).strip()
            number = self._number(chapter, counter)

            return f"""
<div class="fp-exercise">
  <div class="fp-exercise-title">Ejercicio {number}. {title}</div>
  <div class="fp-exercise-content" markdown="1">

{content}

  </div>
</div>
"""

        return pattern.sub(replace, markdown)

    # ---------------------------------------------------------
    # PRÁCTICAS
    # ---------------------------------------------------------

    def _process_practices(self, markdown, chapter):
        counter = 0

        pattern = re.compile(
            r"::: practice\s*\n"
            r"title:\s*(.*?)\s*\n"
            r"difficulty:\s*(.*?)\s*\n"
            r"time:\s*(.*?)\s*\n"
            r"content:\s*\n\n"
            r"(.*?)\n:::",
            re.DOTALL,
        )

        def replace(match):
            nonlocal counter
            counter += 1

            title = match.group(1).strip()
            difficulty = match.group(2).strip()
            time = match.group(3).strip()
            content = match.group(4).strip()
            number = self._number(chapter, counter)

            return f"""
<div class="fp-practice">
  <div class="fp-practice-title">Práctica {number}. {title}</div>
  <div class="fp-practice-meta">
    <span><strong>Dificultad:</strong> {difficulty}</span>
    <span><strong>Tiempo estimado:</strong> {time}</span>
  </div>
  <div class="fp-practice-content" markdown="1">

{content}

  </div>
</div>
"""

        return pattern.sub(replace, markdown)

    # ---------------------------------------------------------
    # ROBOTS DESDE BASE DE CONOCIMIENTO
    # ---------------------------------------------------------

    def _process_robots(self, markdown):
        pattern = re.compile(
            r"::: robot\s*\n"
            r"id:\s*(.*?)\s*\n"
            r":::",
            re.DOTALL,
        )

        def replace(match):
            robot_id = match.group(1).strip()
            robot = self._load_robot(robot_id)

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
    <tr>
      <th>Fabricante</th>
      <td>{robot.get("manufacturer", "No indicado")}</td>
    </tr>
    <tr>
      <th>Usado en</th>
      <td>{used_in}</td>
    </tr>
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

    def _load_robot(self, robot_id):
        return self.kb.get_robot(robot_id)

    # ---------------------------------------------------------
    # UTILIDADES
    # ---------------------------------------------------------

    def _chapter_number(self, path):
        match = re.search(r"capitulo(\d+)\.md", path)
        if match:
            return str(int(match.group(1)))
        return ""

    def _number(self, chapter, counter):
        if chapter:
            return f"{chapter}.{counter}"
        return str(counter)

    def _make_relative_url(self, image_path, page_src_path):
        source_dir = posixpath.dirname(page_src_path)

        target_source_path = posixpath.normpath(
            posixpath.join(source_dir, image_path)
        )

        page_path = Path(page_src_path)

        if page_path.name == "index.md":
            output_dir = posixpath.dirname(page_src_path)
        else:
            output_dir = posixpath.join(
                posixpath.dirname(page_src_path),
                page_path.stem,
            )

        depth = len([part for part in output_dir.split("/") if part])
        prefix = "../" * depth

        return prefix + target_source_path
    
    def on_config(self, config):
        self.kb = KnowledgeBase("knowledge")
        return config
    
    def _process_python_functions(self, markdown):
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
    <div class="fp-robot-card fp-robot-error">
    <strong>Función Python no encontrada:</strong> {function_id}
    </div>
    """

            errors = "\n".join(
                f"<li>{error}</li>" for error in item.get("common_errors", [])
            )

            return f"""
    <div class="fp-python-card">
    <div class="fp-python-title">🐍 {item.get("name", function_id)}</div>

    <p>{item.get("description", "")}</p>

    <p><strong>Sintaxis:</strong></p>

    ```python
    {item.get("syntax", "")}
    
   <p><strong>Devuelve:</strong> {item.get("returns", "")}</p> <p><strong>Errores frecuentes:</strong></p> <ul> {errors} </ul> <p><strong>Ejemplo:</strong></p>
   
   {item.get("example", "")}
   
   
  </div> """ 
  return pattern.sub(replace, markdown)
  