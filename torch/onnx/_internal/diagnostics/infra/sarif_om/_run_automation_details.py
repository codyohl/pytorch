# DO NOT EDIT! This file was generated by jschema_to_python version 0.0.1.dev29,
# with extension for dataclasses and type annotation.

from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass
class RunAutomationDetails(object):
    """Information that describes a run's identity and role within an engineering system process."""

    correlation_guid: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "correlationGuid"}
    )
    description: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "description"}
    )
    guid: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "guid"}
    )
    id: Any = dataclasses.field(default=None, metadata={"schema_property_name": "id"})
    properties: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "properties"}
    )


# flake8: noqa
