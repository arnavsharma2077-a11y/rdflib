"""Regression test for https://github.com/RDFLib/rdflib/issues/748."""

import pytest

from rdflib import Graph
from rdflib.exceptions import ParserError

RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"


def _doc(inner: str) -> bytes:
    return (
        '<?xml version="1.0"?>'
        f'<rdf:RDF xmlns:rdf="{RDF_NS}" xmlns:ex="http://example.org/">'
        '<rdf:Description rdf:about="urn:x">'
        f"<rdf:value>{inner}</rdf:value>"
        "</rdf:Description></rdf:RDF>"
    ).encode()


@pytest.mark.parametrize(
    ["inner", "element"],
    [
        ("<foo/><bar/>", "bar"),
        ("<ex:foo/><ex:bar/>", "bar"),
    ],
)
def test_repeat_node_elements_raise_parser_error(inner: str, element: str) -> None:
    """
    Repeated node elements inside a property element are reported as a
    `ParserError`, also when the element has no namespace.
    """
    with pytest.raises(ParserError) as excinfo:
        Graph().parse(data=_doc(inner), format="xml")
    message = str(excinfo.value)
    assert "Repeat node-elements inside property elements" in message
    assert element in message
