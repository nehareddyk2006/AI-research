import networkx as nx
from pyvis.network import Network


colors = {
    "Model": "#6366F1",
    "Method": "#10B981",
    "Dataset": "#F59E0B",
    "Metric": "#EF4444",
    "Concept": "#8B5CF6",
    "Domain": "#06B6D4",
    "Task": "#EC4899",
    "Problem": "#DC2626",
    "Technique": "#14B8A6",
    "Application": "#F97316",
}


def build_graph(graph_data):

    G = nx.DiGraph()

    # -------------------------
    # Add Nodes
    # -------------------------

    for node in graph_data.get("nodes", []):

        G.add_node(
            node["id"],
            title=f"""
<b>{node['id']}</b><br>
Type: {node['type']}
""",
            color=colors.get(
                node["type"],
                "#94A3B8"
            ),
        )

    # -------------------------
    # Add Edges
    # -------------------------

    for edge in graph_data.get("edges", []):

        G.add_edge(
            edge["source"],
            edge["target"],
            title=edge["relation"],   # hover only
        )

    # -------------------------
    # Node Sizes
    # -------------------------

    for node in G.nodes():

        G.nodes[node]["size"] = (
            18 +
            G.degree(node) * 5
        )

    # -------------------------
    # Build Network
    # -------------------------

    net = Network(
        height="850px",
        width="100%",
        bgcolor="#111111",
        font_color="white",
        directed=True,
    )

    net.from_nx(G)

    net.repulsion(
        node_distance=300,
        spring_length=300,
        central_gravity=0.12,
    )

    net.set_options("""
    const options = {

      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -5000,
          "centralGravity": 0.15,
          "springLength": 260,
          "springConstant": 0.04
        }
      },

      "nodes": {
        "shape": "dot",
        "borderWidth": 2,
        "font": {
          "size": 16,
          "color": "#ffffff"
        }
      },

      "edges": {
        "smooth": {
          "enabled": true,
          "type": "dynamic"
        },
        "arrows": {
          "to": {
            "enabled": true
          }
        }
      },

      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "dragNodes": true,
        "dragView": true,
        "zoomView": true
      }

    }
    """)

    net.save_graph("graph.html")