"""Regression test for https://github.com/RDFLib/rdflib/issues/1785."""

import pytest

from rdflib import Graph, URIRef

EX = "http://example.org/"


@pytest.fixture
def graph() -> Graph:
    g = Graph()
    g.add((URIRef(EX + "a"), URIRef(EX + "p"), URIRef(EX + "x")))
    g.add((URIRef(EX + "b"), URIRef(EX + "p"), URIRef(EX + "y")))
    return g


@pytest.mark.parametrize(
    ["query", "expected_subjects"],
    [
        ("CONSTRUCT WHERE { ?s ?p ?o }", {"a", "b"}),
        ("CONSTRUCT WHERE { ?s ?p ?o } LIMIT 10", {"a", "b"}),
        ("CONSTRUCT WHERE { ?s ?p ?o } LIMIT 1", None),
        ("CONSTRUCT WHERE { ?s ?p ?o } ORDER BY ?s LIMIT 1", {"a"}),
        ("CONSTRUCT WHERE { ?s ?p ?o } ORDER BY DESC(?s) OFFSET 1", {"a"}),
    ],
)
def test_construct_where_with_solution_modifiers(
    graph: Graph, query: str, expected_subjects: "set[str] | None"
) -> None:
    """
    The short form `CONSTRUCT WHERE` works together with `LIMIT`, `OFFSET`
    and `ORDER BY`.
    """
    result = graph.query(query)
    assert result.graph is not None
    subjects = {str(s)[len(EX) :] for s in result.graph.subjects()}
    if expected_subjects is None:
        assert len(result.graph) == 1
        assert subjects <= {"a", "b"}
    else:
        assert subjects == expected_subjects
