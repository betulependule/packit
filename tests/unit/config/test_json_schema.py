# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest
import yaml
from jsonschema import Draft7Validator

from packit.schema import PackageConfigSchema

SCHEMA_DATA_DIR = Path(__file__).parents[2] / "data" / "schema"
VALID_CONFIG_PATHS = sorted((SCHEMA_DATA_DIR / "valid").glob("*.yaml"))
INVALID_CONFIG_PATHS = sorted((SCHEMA_DATA_DIR / "invalid").glob("*.yaml"))


@pytest.fixture(scope="module")
def validator():
    """Return a Draft7 validator for the generated package-config schema."""
    return Draft7Validator(PackageConfigSchema.json_schema())


def _load_yaml(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


@pytest.mark.parametrize(
    "config_path",
    VALID_CONFIG_PATHS,
    ids=lambda path: path.stem,
)
def test_valid_package_configs(validator, config_path):
    """The generated JSON Schema must accept valid .packit.yaml files."""
    errors = list(validator.iter_errors(_load_yaml(config_path)))
    assert errors == []


@pytest.mark.parametrize(
    "config_path",
    INVALID_CONFIG_PATHS,
    ids=lambda path: path.stem,
)
def test_invalid_package_configs(validator, config_path):
    """The generated JSON Schema must reject invalid .packit.yaml files."""
    errors = list(validator.iter_errors(_load_yaml(config_path)))
    assert errors, f"expected validation errors in {config_path.name}"
