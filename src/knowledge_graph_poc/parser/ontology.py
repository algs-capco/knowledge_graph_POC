from importlib.resources import files
from collections.abc import Iterable
from pathlib import Path

from rdflib import Graph, Namespace, OWL, RDF, RDFS, URIRef

from .models import ParseResult


CAPCO = Namespace("https://data.capco.com/kg/ontology/")


def load_ontology() -> Graph:
    """Load the packaged v0.2 ontology into an RDFLib graph."""
    ontology_data = (
        files("knowledge_graph_poc")
        .joinpath("resources", "ontology", "capco_kg_v0_2.ttl")
        .read_bytes()
    )
    graph = Graph()
    try:
        graph.parse(data=ontology_data, format="turtle")
    except Exception as exc:
        raise ValueError(f"Could not parse the packaged v0.2 ontology: {exc}") from exc
    return graph


def build_rdf_graph(
    results: Iterable[ParseResult], ontology: Graph
) -> Graph:
    """Combine the ontology with RDF type assertions found by the parser."""
    graph = Graph()
    for triple in ontology:
        graph.add(triple)

    for result in results:
        file_uri = URIRef(Path(result.file.path).resolve().as_uri())
        file_types: set[URIRef] = set()
        for match in result.matches:
            if match.rdf_type_uri is None:
                continue

            type_uri = URIRef(match.rdf_type_uri)
            if _is_knowledge_asset_type(type_uri, ontology):
                for inherited_type in _inferred_types(type_uri, ontology):
                    graph.add((file_uri, RDF.type, inherited_type))
                    file_types.add(inherited_type)

        for match in result.matches:
            if match.rdf_type_uri is None:
                continue

            entity_type = URIRef(match.rdf_type_uri)
            if _is_knowledge_asset_type(entity_type, ontology):
                continue

            entity_uri = URIRef(match.resource_uri)
            entity_types = _inferred_types(entity_type, ontology)
            for inherited_type in entity_types:
                graph.add((entity_uri, RDF.type, inherited_type))

            for predicate in _matching_relationships(file_types, entity_types, ontology):
                graph.add((file_uri, predicate, entity_uri))

    return graph


def _matching_relationships(
    subject_types: set[URIRef], object_types: set[URIRef], ontology: Graph
) -> set[URIRef]:
    """Find object properties whose declared domain and range fit these types."""
    relationships = set()
    for predicate in ontology.subjects(RDF.type, OWL.ObjectProperty):
        domains = set(ontology.objects(predicate, RDFS.domain))
        ranges = set(ontology.objects(predicate, RDFS.range))
        if domains.intersection(subject_types) and ranges.intersection(object_types):
            relationships.add(predicate)
    return relationships


def _is_knowledge_asset_type(type_uri: URIRef, ontology: Graph) -> bool:
    """Return whether a class is KnowledgeAsset or one of its subclasses."""
    return CAPCO.KnowledgeAsset in _class_ancestors(type_uri, ontology)


def _inferred_types(type_uri: URIRef, ontology: Graph) -> set[URIRef]:
    """Return a class and every superclass reachable in the ontology."""
    ancestors = _class_ancestors(type_uri, ontology)
    return {type_uri, *ancestors}


def _class_ancestors(type_uri: URIRef, ontology: Graph) -> set[URIRef]:
    """Walk rdfs:subClassOf links and return all reachable parent classes."""
    pending = [type_uri]
    visited: set[URIRef] = set()
    while pending:
        current = pending.pop()
        if current in visited:
            continue
        visited.add(current)
        pending.extend(
            parent
            for parent in ontology.objects(current, RDFS.subClassOf)
            if isinstance(parent, URIRef)
        )
    visited.remove(type_uri)
    return visited
