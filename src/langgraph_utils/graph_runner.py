def run_graph(graph, input_data):
    """
    Executes the tasks defined in the graph in sequence.
    """
    current_data = input_data
    for node in graph.nodes:
        current_data = execute_node(node, current_data)
    return current_data

def execute_node(node, input_data):
    """
    Executes a specific node with the given input data.
    """
    if isinstance(node, RetrievalTool):
        result = node.execute(query=input_data)
    elif isinstance(node, WebSearchTool):
        result = node._run(query=input_data)
    elif isinstance(node, TextToMarkdownTool):
        result = node.execute(text=input_data)
    return result
