from pathlib import Path
from typing import Any

import yaml


class KnowledgeBase:
    """
    Gestor centralizado de la base de conocimiento del libro.

    Lee archivos YAML desde la carpeta /knowledge y permite recuperar
    robots, sensores, funciones de Python, comandos de CoppeliaSim, etc.
    """

    def __init__(self, root_path: str = "knowledge"):
        self.root_path = Path(root_path)

    def get_robot(self, robot_id: str) -> dict[str, Any] | None:
        return self._load_yaml("robots", robot_id)

    def get_sensor(self, sensor_id: str) -> dict[str, Any] | None:
        return self._load_yaml("sensors", sensor_id)

    def get_python_function(self, function_id: str) -> dict[str, Any] | None:
        return self._load_yaml("python", function_id)

    def get_coppeliasim_entry(self, entry_id: str) -> dict[str, Any] | None:
        return self._load_yaml("coppeliasim", entry_id)

    def get_glossary_entry(self, entry_id: str) -> dict[str, Any] | None:
        return self._load_yaml("glossary", entry_id)

    def _load_yaml(self, folder: str, item_id: str) -> dict[str, Any] | None:
        path = self.root_path / folder / f"{item_id}.yaml"

        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return data or {}