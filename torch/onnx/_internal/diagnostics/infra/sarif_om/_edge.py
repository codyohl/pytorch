# DO NOT EDIT! This file was generated by jschema_to_python version 0.0.1.dev29,
# with extension for dataclasses and type annotation.

from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass
class Edge(object):
    """Represents a directed edge in a graph."""

    id: Any = dataclasses.field(metadata={"schema_property_name": "id"})
    source_node_id: Any = dataclasses.field(
        metadata={"schema_property_name": "sourceNodeId"}
    )
    target_node_id: Any = dataclasses.field(
        metadata={"schema_property_name": "targetNodeId"}
    )
    label: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "label"}
    )
    properties: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "properties"}
    )


# flake8: noqa
