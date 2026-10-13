from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS

from .models import RegexPattern


CAPCO = Namespace("https://data.capco.com/kg/ontology/")


def load_patterns(ttl_path: str | Path) -> list[RegexPattern]:
    """Load regex rules from SeedItem resources in a Turtle file."""
    ttl_path = Path(ttl_path)
    graph = Graph()
    try:
        graph.parse(ttl_path, format="turtle")
    except Exception as exc:
        raise ValueError(f"Could not parse Turtle file {ttl_path}: {exc}") from exc

    patterns = []
    for resource in sorted(graph.subjects(RDF.type, CAPCO.SeedItem), key=str):
        regex = graph.value(resource, CAPCO.aliasToken)
        if regex is None:
            raise ValueError(f"Missing regex (capco:aliasToken) for {resource}")
        name = graph.value(resource, CAPCO.canonicalLabel) or graph.value(resource, RDFS.label)
        target = graph.value(resource, CAPCO.target)
        rdf_type = next(
            (
                seed_type
                for seed_type in graph.objects(resource, RDF.type)
                if seed_type != CAPCO.SeedItem
            ),
            None,
        )
        patterns.append(
            RegexPattern(
                name=str(name) if name is not None else str(resource),
                target=str(target) if target is not None else "name",
                regex=str(regex),
                resource_uri=str(resource),
                rdf_type_uri=str(rdf_type) if rdf_type is not None else None,
            )
        )
    return patterns
