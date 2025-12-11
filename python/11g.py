import networkx as nx
import matplotlib.pyplot as plt

def read_graph(filename):
    G = nx.DiGraph()
    with open(filename, 'r') as f:
        for line in f:
            # Clean and skip empty/comment lines
            line = line.strip()
            if not line or ':' not in line:
                continue
            src, dsts = line.split(':', 1)
            src = src.strip()
            dsts = dsts.strip()
            if dsts:
                for dst in dsts.split():
                    G.add_edge(src, dst)
            else:
                # Node with no edges
                G.add_node(src)
    return G

def draw_graph(G):
    # For nicer large graph drawing, spring layout can be slow and messy. Try kamada_kawai.
    pos = nx.kamada_kawai_layout(G)
    plt.figure(figsize=(16, 16))
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=500, alpha=0.7)
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=15, width=1.2, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=9)
    plt.axis('off')
    plt.title("Graph from day11a.txt")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    G = read_graph("res/day11.txt")
    draw_graph(G)
