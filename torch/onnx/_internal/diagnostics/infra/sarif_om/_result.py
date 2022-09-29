# DO NOT EDIT! This file was generated by jschema_to_python version 0.0.1.dev29,
# with extension for dataclasses and type annotation.

from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass
class Result(object):
    """A result produced by an analysis tool."""

    message: Any = dataclasses.field(metadata={"schema_property_name": "message"})
    analysis_target: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "analysisTarget"}
    )
    attachments: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "attachments"}
    )
    baseline_state: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "baselineState"}
    )
    code_flows: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "codeFlows"}
    )
    correlation_guid: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "correlationGuid"}
    )
    fingerprints: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "fingerprints"}
    )
    fixes: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "fixes"}
    )
    graph_traversals: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "graphTraversals"}
    )
    graphs: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "graphs"}
    )
    guid: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "guid"}
    )
    hosted_viewer_uri: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "hostedViewerUri"}
    )
    kind: Any = dataclasses.field(
        default="fail", metadata={"schema_property_name": "kind"}
    )
    level: Any = dataclasses.field(
        default="warning", metadata={"schema_property_name": "level"}
    )
    locations: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "locations"}
    )
    occurrence_count: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "occurrenceCount"}
    )
    partial_fingerprints: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "partialFingerprints"}
    )
    properties: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "properties"}
    )
    provenance: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "provenance"}
    )
    rank: Any = dataclasses.field(
        default=-1.0, metadata={"schema_property_name": "rank"}
    )
    related_locations: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "relatedLocations"}
    )
    rule: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "rule"}
    )
    rule_id: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "ruleId"}
    )
    rule_index: Any = dataclasses.field(
        default=-1, metadata={"schema_property_name": "ruleIndex"}
    )
    stacks: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "stacks"}
    )
    suppressions: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "suppressions"}
    )
    taxa: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "taxa"}
    )
    web_request: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "webRequest"}
    )
    web_response: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "webResponse"}
    )
    work_item_uris: Any = dataclasses.field(
        default=None, metadata={"schema_property_name": "workItemUris"}
    )


# flake8: noqa
