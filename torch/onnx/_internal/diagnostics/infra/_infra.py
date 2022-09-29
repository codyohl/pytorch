"""This file defines an additional layer of abstraction on top of the SARIF OM."""

from __future__ import annotations

import dataclasses
import enum
from typing import Any, FrozenSet, List, Optional, Sequence, Set, Tuple, Type, TypeVar

from torch.onnx._internal.diagnostics.infra import formatter, sarif_om


class Level(enum.Enum):
    """The level of a diagnostic."""

    NONE = "none"
    NOTE = "note"
    WARNING = "warning"
    ERROR = "error"


levels = Level


@dataclasses.dataclass(frozen=True)
class Rule:
    id: str
    name: str
    message_default_template: str
    short_description: Optional[str] = None
    full_description: Optional[str] = None
    help_uri: Optional[str] = None

    @classmethod
    def from_sarif(cls, **kwargs) -> Rule:
        """Returns a rule from the SARIF reporting descriptor."""
        short_description = (
            kwargs["short_description"]["text"]
            if "short_description" in kwargs
            else None
        )
        full_description = (
            kwargs["full_description"]["markdown"]
            if "full_description" in kwargs
            else None
        )
        help_uri = kwargs["help_uri"] if "help_uri" in kwargs else None

        rule = cls(
            id=kwargs["id"],
            name=kwargs["name"],
            message_default_template=kwargs["message_strings"]["default"]["text"],
            short_description=short_description,
            full_description=full_description,
            help_uri=help_uri,
        )
        return rule

    def sarif(self) -> sarif_om.ReportingDescriptor:
        """Returns a SARIF reporting descriptor of this Rule."""
        short_description = (
            sarif_om.MultiformatMessageString(text=self.short_description)
            if self.short_description is not None
            else None
        )
        full_description = (
            sarif_om.MultiformatMessageString(text="", markdown=self.full_description)
            if self.full_description is not None
            else None
        )
        return sarif_om.ReportingDescriptor(
            id=self.id,
            name=self.name,
            short_description=short_description,
            full_description=full_description,
            help_uri=self.help_uri,
        )


@dataclasses.dataclass
class Location:
    uri: str
    message: str
    line: Optional[int] = None
    start_column: Optional[int] = None
    end_column: Optional[int] = None

    def sarif(self) -> sarif_om.Location:
        """Returns the SARIF representation of this location."""
        return sarif_om.Location(
            physical_location=sarif_om.PhysicalLocation(
                artifact_location=sarif_om.ArtifactLocation(uri=self.uri),
                region=sarif_om.Region(
                    start_line=self.line,
                    start_column=self.start_column,
                    end_line=self.line,
                    end_column=self.end_column,
                ),
            ),
            message=sarif_om.Message(text=self.message),
        )


@dataclasses.dataclass
class Stack:
    frame_locations: List[Location] = dataclasses.field(default_factory=list)

    def sarif(self) -> sarif_om.Stack:
        """Returns the SARIF representation of this stack."""
        return sarif_om.Stack(
            frames=[
                sarif_om.StackFrame(location=loc.sarif())
                for loc in self.frame_locations
            ]
        )

    def add_frame(
        self,
        uri: str,
        message: str,
        line: Optional[int] = None,
        start_column: Optional[int] = None,
        end_column: Optional[int] = None,
    ) -> None:
        """Adds a frame to the stack."""
        self.frame_locations.append(
            Location(
                uri=uri,
                message=message,
                line=line,
                start_column=start_column,
                end_column=end_column,
            )
        )


# This is a workaround for mypy not supporting Self from typing_extensions.
_Diagnostic = TypeVar("_Diagnostic", bound="Diagnostic")


@dataclasses.dataclass
class Diagnostic:
    rule: Rule
    level: Level
    message_args: Optional[Tuple[Any, ...]]
    locations: List[Location] = dataclasses.field(default_factory=list)
    stacks: List[Stack] = dataclasses.field(default_factory=list)
    additional_message: Optional[str] = None

    def sarif(self) -> sarif_om.Result:
        """Returns the SARIF Result representation of this diagnostic."""
        if self.message_args is None:
            self.message_args = tuple()
        message = self.rule.message_default_template.format(*self.message_args)
        if self.additional_message is not None:
            message = f"{message}\n{self.additional_message}"
        sarif_result = sarif_om.Result(
            message=sarif_om.Message(text=message),
            level=self.level.value,
            rule_id=self.rule.id,
        )
        sarif_result.locations = [location.sarif() for location in self.locations]
        sarif_result.stacks = [stack.sarif() for stack in self.stacks]
        return sarif_result

    def with_location(self: _Diagnostic, location: Location) -> _Diagnostic:
        """Adds a location to the diagnostic."""
        self.locations.append(location)
        return self

    def with_stack(self: _Diagnostic, stack: Stack) -> _Diagnostic:
        """Adds a stack to the diagnostic."""
        self.stacks.append(stack)
        return self

    def with_additional_message(self: _Diagnostic, message: str) -> _Diagnostic:
        """Adds an additional message to the diagnostic."""
        if self.additional_message is None:
            self.additional_message = message
        else:
            self.additional_message = f"{self.additional_message}\n{message}"
        return self


@dataclasses.dataclass
class RuleCollection:
    _rule_id_name_set: FrozenSet[Tuple[str, str]] = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self._rule_id_name_set = frozenset(
            {
                (field.default.id, field.default.name)
                for field in dataclasses.fields(self)
                if isinstance(field.default, Rule)
            }
        )

    def __contains__(self, rule: Rule) -> bool:
        """Checks if the rule is in the collection."""
        return (rule.id, rule.name) in self._rule_id_name_set

    @classmethod
    def custom_collection_from_list(
        cls, new_collection_class_name: str, rules: Sequence[Rule]
    ) -> RuleCollection:
        """Creates a custom class inherited from RuleCollection with the list of rules."""
        return dataclasses.make_dataclass(
            new_collection_class_name,
            [
                (
                    formatter._kebab_case_to_snake_case(rule.name),
                    type(rule),
                    dataclasses.field(default=rule),
                )
                for rule in rules
            ],
            bases=(cls,),
        )()


@dataclasses.dataclass(frozen=True)
class DiagnosticTool:
    name: str
    version: str
    rules: RuleCollection
    diagnostic_type: Type[Diagnostic] = dataclasses.field(default=Diagnostic)
    _triggered_rules: Set[Rule] = dataclasses.field(init=False, default_factory=set)

    def __post_init__(self) -> None:
        if not issubclass(self.diagnostic_type, Diagnostic):
            raise TypeError(
                "Expected diagnostic_type to be a subclass of Diagnostic, "
                f"but got {self.diagnostic_type}"
            )

    def sarif(self) -> sarif_om.Tool:
        """Returns the SARIF Tool representation."""
        return sarif_om.Tool(
            driver=sarif_om.ToolComponent(
                name=self.name,
                version=self.version,
                rules=[rule.sarif() for rule in self._triggered_rules],
            )
        )

    def create_diagnostic(
        self,
        rule: Rule,
        level: Level,
        message_args: Optional[Tuple[Any, ...]],
        **kwargs,
    ) -> Diagnostic:
        """Creates a diagnostic for the given arguments.

        Args:
            rule: The rule that triggered the diagnostic.
            level: The level of the diagnostic.
            message_args: The arguments to format the rule's message template.
            **kwargs: Additional arguments to pass to the Diagnostic constructor.

        Returns:
            The created diagnostic.

        Raises:
            ValueError: If the rule is not supported by the tool.
        """
        if rule not in self.rules:
            raise ValueError(
                f"Rule '{rule.id}:{rule.name}' is not supported by this tool '{self.name} {self.version}'."
                f" Supported rules are: {self.rules._rule_id_name_set}"
            )
        self._triggered_rules.add(rule)
        return self.diagnostic_type(rule, level, message_args, **kwargs)


class Invocation:
    # TODO: Implement this.
    pass


@dataclasses.dataclass
class DiagnosticOptions:
    """
    Options for diagnostic context.
    """


@dataclasses.dataclass
class DiagnosticContext:
    tool: DiagnosticTool
    options: Optional[DiagnosticOptions] = None
    _diagnostics: List[Diagnostic] = dataclasses.field(init=False, default_factory=list)
    _invocation: Invocation = dataclasses.field(init=False)
    _is_active: bool = dataclasses.field(init=False, default=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

    def sarif(self) -> sarif_om.Run:
        """Returns the SARIF Run object."""
        return sarif_om.Run(
            tool=self.tool.sarif(),
            results=[diagnostic.sarif() for diagnostic in self._diagnostics],
        )

    def diagnose(
        self,
        rule: Rule,
        level: Level,
        message_args: Optional[Tuple[Any, ...]] = None,
        **kwargs,
    ) -> Diagnostic:
        """Creates a diagnostic for the given arguments.

        Args:
            rule: The rule that triggered the diagnostic.
            level: The level of the diagnostic.
            message_args: The arguments to format the rule's message template.
            **kwargs: Additional arguments to pass to the Diagnostic constructor.

        Returns:
            The created diagnostic.

        Raises:
            RuntimeError: If the context is not active.
            ValueError: If the rule is not supported by the tool.
        """
        if not self._is_active:
            raise RuntimeError("The diagnostics context is not active.")

        diagnostic = self.tool.create_diagnostic(rule, level, message_args, **kwargs)
        self._diagnostics.append(diagnostic)
        return diagnostic
