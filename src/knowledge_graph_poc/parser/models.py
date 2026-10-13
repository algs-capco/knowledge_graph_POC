import re
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class FileReference:
    path: str
    name: str


@dataclass(frozen=True)
class RegexPattern:
    name: str
    target: Literal["path", "name"]
    regex: str
    resource_uri: str
    rdf_type_uri: str | None = None

    def __post_init__(self) -> None:
        if self.target not in ("path", "name"):
            raise ValueError(f"Unknown pattern target {self.target!r}")
        try:
            re.compile(self.regex)
        except re.error as exc:
            raise ValueError(f"Invalid regex for pattern {self.name!r}: {exc}") from exc


@dataclass(frozen=True)
class PatternMatch:
    pattern_name: str
    groups: dict[str, str]
    resource_uri: str
    rdf_type_uri: str | None = None


@dataclass(frozen=True)
class ParseResult:
    file: FileReference
    matches: list[PatternMatch]
