# Knowledge Graph POC

Python package for a knowledge graph proof of concept. The project is managed with [`uv`](https://docs.astral.sh/uv/).

## Getting started

Install the project and its dependencies into the project environment:

```sh
uv sync
```

Run the starter command:

```sh
uv run knowledge-graph-poc
```

Run the test suite:

```sh
uv run pytest
```

The package source is in `src/knowledge_graph_poc/`. Add runtime dependencies with `uv add <package>`.

## Knowledge asset types

The v0.2 ontology models reusable business content as `KnowledgeAsset`, including:

- `Document`, with subtypes `RFPResponse`, `RFIResponse`, `Proposal`, and `Presentation`
- `Proposition`
- `Credential`, with subtype `CaseStudy`

`FileObject` represents the physical file in its source system. `KnowledgeAsset` represents the business content associated with that file.
