import json
from pathlib import Path

import pytest

from organization_workspace import OrganizationWorkspace
from settings import ServerSettings


def _reset_workspace_state() -> None:
    OrganizationWorkspace.available = False
    OrganizationWorkspace.project_id_by_path = {}
    OrganizationWorkspace.mount_source = None
    OrganizationWorkspace.mount_destination = None
    OrganizationWorkspace.MOUNT_SOURCE = None
    OrganizationWorkspace.MOUNT_DESTINATION = None
    OrganizationWorkspace._legacy_warning_emitted = False


@pytest.fixture(autouse=True)
def reset_workspace() -> None:
    _reset_workspace_state()
    yield
    _reset_workspace_state()


def test_configure_sets_legacy_attributes(tmp_path: Path) -> None:
    mount_source = tmp_path / "source"
    mount_dest = tmp_path / "dest"
    mount_source.mkdir()
    mount_dest.mkdir()
    settings = ServerSettings(
        mount_source_path=str(mount_source),
        mount_destination_path=str(mount_dest),
    )

    with pytest.warns(DeprecationWarning):
        OrganizationWorkspace.configure(settings)

    assert OrganizationWorkspace.mount_source == mount_source.resolve()
    assert OrganizationWorkspace.mount_destination == mount_dest.resolve()
    assert OrganizationWorkspace.MOUNT_SOURCE == str(mount_source.resolve())
    assert OrganizationWorkspace.MOUNT_DESTINATION == str(mount_dest.resolve())


def test_load_populates_project_ids(tmp_path: Path) -> None:
    mount_source = tmp_path / "source"
    mount_dest = tmp_path / "dest"
    project_dir = mount_dest / "ProjectA"
    ignored_dir = mount_dest / "data"
    mount_source.mkdir()
    mount_dest.mkdir()
    project_dir.mkdir()
    ignored_dir.mkdir()
    (project_dir / "config.json").write_text(json.dumps({"cloud-id": "123"}))
    (ignored_dir / "config.json").write_text(json.dumps({"cloud-id": "ignored"}))
    settings = ServerSettings(
        mount_source_path=str(mount_source),
        mount_destination_path=str(mount_dest),
    )

    with pytest.warns(DeprecationWarning):
        OrganizationWorkspace.load(settings)

    assert OrganizationWorkspace.available is True
    expected_path = str(project_dir.resolve())
    assert OrganizationWorkspace.project_id_by_path == {expected_path: "123"}
