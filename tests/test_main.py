from knowledge_graph_poc import main
from knowledge_graph_poc.parser import FileReference, load_patterns, parse_files
from pathlib import Path

import pytest


def test_rules_match_document_type_in_a_real_file_path():
    ontology_dir = (
        Path(__file__).parent.parent
        / "src"
        / "knowledge_graph_poc"
        / "resources"
        / "ontology"
    )
    rules = load_patterns(ontology_dir / "seeds-upload.ttl")
    file_path = Path(__file__).parent / "resources" / "test_file_system" / "HSBC" / "Rfps" / "HSBC_RFP_2026.docx"
    file = FileReference(path=str(file_path), name=file_path.name)

    result = parse_files([file], rules)[0]

    hsbc_match = next(
        match for match in result.matches if match.pattern_name == "HSBC"
    )
    rfp_match = next(
        match for match in result.matches if match.pattern_name == "RFPResponse"
    )

    # RDF-shaped tuple: (subject, predicate, object). The document's detected
    # type and the matched client seed are both taken from the seed file.
    rdf_tuple = (
        str(file_path),
        hsbc_match.rdf_type_uri,
        hsbc_match.resource_uri,
    )
    document_type_tuple = (
        str(file_path),
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
        rfp_match.rdf_type_uri,
    )

    assert hsbc_match.rdf_type_uri == "https://data.capco.com/kg/ontology/Client"
    assert rdf_tuple == (
        str(file_path),
        "https://data.capco.com/kg/ontology/Client",
        "https://data.capco.com/kg/asset/seed-hsbc",
    )
    assert document_type_tuple[2] == "https://data.capco.com/kg/ontology/RFPResponse"
