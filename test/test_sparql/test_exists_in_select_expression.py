"""Regression test for https://github.com/RDFLib/rdflib/issues/2124."""

import pytest

from rdflib import XSD, Graph, Literal, URIRef

EX = "http://example.org/"


@pytest.fixture
def graph() -> Graph:
    g = Graph()
    g.add((URIRef(EX + "a"), URIRef(EX + "b"), URIRef(EX + "c")))
    return g


@pytest.mark.parametrize(
    ["query", "expected"],
    [
        (
            "SELECT (EXISTS { <http://example.org/a> <http://example.org/b> "
            "<http://example.org/c> } AS ?x) {}",
            True,
        ),
        (
            "SELECT (EXISTS { <http://example.org/a> <http://example.org/b> "
            "<http://example.org/nope> } AS ?x) {}",
            False,
        ),
        (
            "SELECT (NOT EXISTS { <http://example.org/a> <http://example.org/b> "
            "<http://example.org/c> } AS ?x) {}",
            False,
        ),
        (
            "SELECT (EXISTS { ?s <http://example.org/b> <http://example.org/c> } AS ?x) "
            "{ VALUES ?s { <http://example.org/a> } }",
            True,
        ),
        (
            "SELECT (!EXISTS { <http://example.org/a> <http://example.org/b> "
            "<http://example.org/nope> } AS ?x) {}",
            True,
        ),
    ],
)
def test_exists_in_select_expression(graph: Graph, query: str, expected: bool) -> None:
    """`EXISTS` and `NOT EXISTS` can be used in a `SELECT (expr AS ?var)`."""
    rows = list(graph.query(query))
    assert rows == [(Literal(expected, datatype=XSD.boolean),)]
