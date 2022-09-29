# DO NOT EDIT! This file was generated by jschema_to_python version 0.0.1.dev29,
# with extension for dataclasses and type annotation.

from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass
class WebResponse(object):
    """Describes the response to an HTTP request."""

    body: Any
    headers: Any
    index: Any
    no_response_received: Any
    properties: Any
    protocol: Any
    reason_phrase: Any
    status_code: Any
    version: Any


# flake8: noqa
