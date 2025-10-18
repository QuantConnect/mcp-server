from __future__ import annotations

import json
from pathlib import Path

from settings import ServerSettings, get_settings


IGNORED_ENTRIES = {".QuantConnect", "data", "lean.json"}


class OrganizationWorkspace:
    """Helper for mapping local Lean project paths to QuantConnect project IDs."""

    available = False
    project_id_by_path: dict[str, str] = {}
    mount_source: Path | None = None
    mount_destination: Path | None = None

    # Backwards compatibility with legacy attribute names.
    MOUNT_SOURCE: str | None = None
    MOUNT_DESTINATION: str | None = None

    @classmethod
    def configure(cls, settings: ServerSettings | None = None) -> None:
        """Store mount configuration derived from the provided settings."""

        settings = settings or get_settings()
        cls.mount_source = settings.mount_source
        cls.mount_destination = settings.mount_destination
        cls.MOUNT_SOURCE = str(cls.mount_source) if cls.mount_source else None
        cls.MOUNT_DESTINATION = (
            str(cls.mount_destination) if cls.mount_destination else None
        )

    @classmethod
    def load(cls, settings: ServerSettings | None = None) -> None:
        """Populate project mappings when a workspace mount is available."""

        cls.configure(settings)
        cls.project_id_by_path = {}

        destination = cls.mount_destination
        if not destination or not destination.exists():
            cls.available = False
            return

        for entry in destination.iterdir():
            if entry.name in IGNORED_ENTRIES:
                continue
            cls._process_directory(entry)
        cls.available = True

    @classmethod
    def _process_directory(cls, path: Path) -> None:
        """Recursively collect project identifiers from Lean config files."""

        if not path.is_dir():
            return

        config_path = path / "config.json"
        if config_path.is_file():
            with config_path.open("r", encoding="utf-8") as handle:
                config_data = json.load(handle)
            cloud_id = config_data.get("cloud-id")
            if cloud_id:
                cls.project_id_by_path[str(path)] = cloud_id
            return

        for child in path.iterdir():
            if child.is_dir():
                cls._process_directory(child)
