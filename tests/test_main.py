from knowledge_graph_poc.parser import (
    FileReference,
    build_rdf_graph,
    load_ontology,
    load_patterns,
    parse_files,
)
from pathlib import Path
from rdflib import Namespace, RDF, RDFS, URIRef


CAPCO = Namespace("https://data.capco.com/kg/ontology/")


def test_hsbc_rfp():
    ontology_dir = (
        Path(__file__).parent.parent
        / "src"
        / "knowledge_graph_poc"
        / "resources"
        / "ontology"
    )
    rules = load_patterns(ontology_dir / "seeds-upload.ttl")
    file_path = (
        Path(__file__).parent
        / "resources"
        / "test_file_system"
        / "HSBC"
        / "Rfps"
        / "HSBC_RFP_2026.docx"
    )
    assert file_path.is_file()
    file = FileReference(path=str(file_path), name=file_path.name)

    results = parse_files([file], rules)
    ontology = load_ontology()
    graph = build_rdf_graph(results, ontology)
    file_uri = URIRef(file_path.resolve().as_uri())
    hsbc_seed_uri = URIRef("https://data.capco.com/kg/asset/seed-hsbc")

    assert (file_uri, RDF.type, CAPCO.RFPResponse) in graph
    assert (file_uri, RDF.type, CAPCO.Document) in graph
    assert (file_uri, RDF.type, CAPCO.KnowledgeAsset) in graph
    assert (CAPCO.RFPResponse, RDFS.subClassOf, CAPCO.Document) in graph
    assert (CAPCO.Document, RDFS.subClassOf, CAPCO.KnowledgeAsset) in graph
    assert (file_uri, CAPCO.aboutClient, hsbc_seed_uri) in graph

def test_hsbc_presentation():
    ontology_dir = (
        Path(__file__).parent.parent
        / "src"
        / "knowledge_graph_poc"
        / "resources"
        / "ontology"
    )
    rules = load_patterns(ontology_dir / "seeds-upload.ttl")
    file_path = (
        Path(__file__).parent
        / "resources"
        / "test_file_system"
        / "HSBC"
        / "credentials"
        / "GL hrs cred.pptx"
    )
    assert file_path.is_file()
    file = FileReference(path=str(file_path), name=file_path.name)

    results = parse_files([file], rules)
    ontology = load_ontology()
    graph = build_rdf_graph(results, ontology)
    file_uri = URIRef(file_path.resolve().as_uri())
    hsbc_seed_uri = URIRef("https://data.capco.com/kg/asset/seed-hsbc")

    assert (file_uri, RDF.type, CAPCO.Presentation) in graph
    assert (file_uri, RDF.type, CAPCO.Document) in graph
    assert (file_uri, RDF.type, CAPCO.KnowledgeAsset) in graph
    assert (CAPCO.Presentation, RDFS.subClassOf, CAPCO.Document) in graph
    assert (CAPCO.Document, RDFS.subClassOf, CAPCO.KnowledgeAsset) in graph
    assert (file_uri, CAPCO.aboutClient, hsbc_seed_uri) in graph

def test_hsbc_cred():
    ontology_dir = (
            Path(__file__).parent.parent
            / "src"
            / "knowledge_graph_poc"
            / "resources"
            / "ontology"
        )
    rules = load_patterns(ontology_dir / "seeds-upload.ttl")
    file_path = (
        Path(__file__).parent
        / "resources"
        / "test_file_system"
        / "HSBC"
        / "credentials"
        / "GL hrs cred.pptx"
    )
    assert file_path.is_file()
    file = FileReference(path=str(file_path), name=file_path.name)

    results = parse_files([file], rules)
    ontology = load_ontology()
    graph = build_rdf_graph(results, ontology)
    file_uri = URIRef(file_path.resolve().as_uri())
    hsbc_seed_uri = URIRef("https://data.capco.com/kg/asset/seed-hsbc")

    assert (file_uri, RDF.type, CAPCO.Credential) in graph
    assert not (file_uri, RDF.type, CAPCO.RFPResponse) in graph
    assert (file_uri, RDF.type, CAPCO.Document) in graph
    assert (file_uri, RDF.type, CAPCO.KnowledgeAsset) in graph
    assert (CAPCO.Credential, RDFS.subClassOf, CAPCO.KnowledgeAsset) in graph
    assert (file_uri, CAPCO.aboutClient, hsbc_seed_uri) in graph

def test_neso_rfp():
    ontology_dir = (
        Path(__file__).parent.parent
        / "src"
        / "knowledge_graph_poc"
        / "resources"
        / "ontology"
    )
    rules = load_patterns(ontology_dir / "seeds-upload.ttl")
    file_path = (
        Path(__file__).parent
        / "resources"
        / "test_file_system"
        / "NESO"
        / "RFP_NESO_26.docx"
    )
    assert file_path.is_file()
    file = FileReference(path=str(file_path), name=file_path.name)

    results = parse_files([file], rules)
    ontology = load_ontology()
    graph = build_rdf_graph(results, ontology)
    file_uri = URIRef(file_path.resolve().as_uri())
    nesso_seed_uri = URIRef("https://data.capco.com/kg/asset/seed-neso")

    assert (file_uri, RDF.type, CAPCO.RFPResponse) in graph
    assert (file_uri, RDF.type, CAPCO.Document) in graph
    assert (file_uri, RDF.type, CAPCO.KnowledgeAsset) in graph
    assert (CAPCO.RFPResponse, RDFS.subClassOf, CAPCO.Document) in graph
    assert (CAPCO.Document, RDFS.subClassOf, CAPCO.KnowledgeAsset) in graph
    assert (file_uri, CAPCO.aboutClient, nesso_seed_uri) in graph