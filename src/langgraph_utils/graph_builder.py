from langgraph import Graph
from langgraph_utils.node_definitions import RetrievalTool, WebSearchTool, TextToMarkdownTool

def build_graph(selected_tools):
    """
    Builds a graph using the selected tools.
    """
    # Initialize the graph
    graph = Graph(name="Task Workflow")

    # Add tools as nodes to the graph
    nodes = {}
    for tool in selected_tools:
        if tool == 'retriever':
            node = RetrievalTool()
        elif tool == 'web_search':
            node = WebSearchTool()
        elif tool == 'text_to_html':
            node = TextToMarkdownTool()

        nodes[tool] = node
        graph.add_node(node)

    # Define edges (task dependencies)
    if 'retriever' in nodes and 'web_search' in nodes:
        graph.add_edge(nodes['retriever'], nodes['web_search'])
    
    if 'web_search' in nodes and 'text_to_html' in nodes:
        graph.add_edge(nodes['web_search'], nodes['text_to_html'])
    
    return graph
