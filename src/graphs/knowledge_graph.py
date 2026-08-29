def build_graph(graph_data):
    """
    Prepare knowledge graph data for the React frontend.

    The AI analyzer generates the graph structure as:
    {
        "nodes": [
            {
                "id": "...",
                "type": "..."
            }
        ],
        "edges": [
            {
                "source": "...",
                "target": "...",
                "relation": "..."
            }
        ]
    }

    The frontend is responsible for rendering the graph.
    """

    if not isinstance(graph_data, dict):
        return {
            "nodes": [],
            "edges": [],
        }

    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    clean_nodes = []

    for node in nodes:

        if not isinstance(node, dict):
            continue

        node_id = node.get("id")

        if not node_id:
            continue

        clean_nodes.append({
            "id": str(node_id),
            "type": node.get(
                "type",
                "Concept"
            ),
        })


    clean_edges = []

    for edge in edges:

        if not isinstance(edge, dict):
            continue

        source = edge.get("source")
        target = edge.get("target")

        if not source or not target:
            continue

        clean_edges.append({
            "source": str(source),
            "target": str(target),
            "relation": edge.get(
                "relation",
                "related to"
            ),
        })


    return {
        "nodes": clean_nodes,
        "edges": clean_edges,
    }