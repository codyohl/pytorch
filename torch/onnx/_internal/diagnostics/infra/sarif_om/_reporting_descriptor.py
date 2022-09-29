# DO NOT EDIT! This file was generated by jschema_to_python version 0.0.1.dev29,
# with extension for dataclasses and type annotation.

from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass
class ReportingDescriptor(object):
    """Metadata that describes a specific report produced by the tool, as part of the analysis it provides or its runtime reporting."""

    id: Any
    default_configuration: Any
    deprecated_guids: Any
    deprecated_ids: Any
    deprecated_names: Any
    full_description: Any
    guid: Any
    help: Any
    help_uri: Any
    message_strings: Any
    name: Any
    properties: Any
    relationships: Any
    short_description: Any


# flake8: noqa
