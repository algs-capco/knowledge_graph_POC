import re
from collections.abc import Iterable

from .models import FileReference, ParseResult, PatternMatch, RegexPattern


def parse_files(
    files: Iterable[FileReference], patterns: Iterable[RegexPattern]
) -> list[ParseResult]:
    """Apply loaded rules to each file's full path."""
    pattern_list = list(patterns)
    results = []
    for file in files:
        matches = []
        for pattern in pattern_list:
            match = re.search(pattern.regex, file.path)
            if match is not None:
                matches.append(
                    PatternMatch(
                        pattern.name,
                        match.groupdict(),
                        pattern.resource_uri,
                        pattern.rdf_type_uri,
                    )
                )
        results.append(ParseResult(file, matches))
    return results
