from decimal import Decimal
from .xml_utils import NodeNotFoundError

def ensure_decimal(value):
    return value if isinstance(value, Decimal) else Decimal(value)


def first_child_by_localname(node, localname):
    """Return the first child element whose localName matches, ignoring prefixes."""
    for child in getattr(node, "childNodes", []):
        if child.nodeType == child.ELEMENT_NODE:
            # localName is None for non-namespaced elements; fall back to tagName
            ln = getattr(child, "localName", None) or child.tagName
            # handle both "requestIdentifier" and "ns2:requestIdentifier"
            if ln == localname or ln.endswith(":" + localname):
                return child
    raise NodeNotFoundError(f"Child with local name '{localname}' not found")
        