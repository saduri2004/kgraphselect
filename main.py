from typing import List
from graph.node import Node
from graph.graph import Graph
from openai import OpenAI
import os

def initialize_graph() -> Graph:
    """
    Initialize a new graph with a start and end node.
    """
    graph = Graph()
    graph.add_node(0, content="Start Node", is_start=True)
    graph.add_node(-1, content="End Node", is_end=True)
    return graph

def process_sequences(sequences: List[List[str]], graph: Graph) -> List[List[Node]]:
    """
    Convert a list of sequences (list of strings) into a list of Node objects.
    If a node does not already exist in the graph, add it.
    
    :param sequences: List of sequences, where each sequence is a list of strings (actions).
    :param graph: The Graph object to populate with nodes.
    :return: List of sequences, where each sequence is a list of Node objects.
    """
    processed_sequences = []
    for seq in sequences:
        processed_seq = []
        for action in seq:
            # Check if the action exists in the graph
            if action not in graph.node_actions:
                # Assign a unique ID and add the node to the graph
                graph.node_actions.add(action)
                node_id = len(graph.nodes)  # Unique ID for the new node
                graph.add_node(node_id, content=action)
            node = next(node for node in graph.nodes.values() if node.content == action)
            processed_seq.append(node)
        processed_sequences.append(processed_seq)
    return processed_sequences

def extract_nodes_and_edges(sequences: List[List[Node]], graph: Graph):
    """
    From a list of action sequences, construct a topological action graph with nodes and edges.
    
    :param sequences: List of sequences, where each sequence is a list of Node objects.
    :param graph: The Graph object to update with edges.
    """
    start_node = graph.get_start_node()
    end_node = graph.get_end_node()

    for seq in sequences:
        print(f"Processing sequence: {[node.content for node in seq]}")

        for i, step in enumerate(seq):
            # Connect the first node in the sequence to the start node
            if i == 0:
                graph.add_edge(start_node.node_id, step.node_id)
                print(f"Added edge from '{start_node.node_id}' to '{step.node_id}'")

            # Connect subsequent nodes in the sequence
            if i < len(seq) - 1:
                next_step = seq[i + 1]
                graph.add_edge(step.node_id, next_step.node_id)
                print(f"Added edge from '{step.node_id}' to '{next_step.node_id}'")

            # Connect the last node in the sequence to the end node
            if i == len(seq) - 1:
                graph.add_edge(step.node_id, end_node.node_id)
                print(f"Added edge from '{step.node_id}' to end node '{end_node.node_id}'")

def pick_next_node(current_node: str, next_nodes: List[dict[str, any]], query_content:str): 
    #use an llm completion call to gpt-4o to select the proper next step based on the current accumulated state
    openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    user_prompt = (
        "You are trying to figure out the next step in a sequence of actions based on the query."
    )
    user_prompt += "The current step is" + current_node
    user_prompt += "The possible next steps are" + next_nodes
    user_prompt += "The query is" + query_content
    user_prompt += """Pick the next step based on the current context. Return the id of the next step as the last character 
    of your response""" 

    messages = [
        {"role": "system", "content": "You are trying to figure out the next step in a sequence of actions. Respond appropriately based on the current context."},
        {"role": "user", "content": user_prompt},
    ]
    response = openai.chat.completions.create(
        model="gpt-4", messages=messages, max_tokens=400, temperature=0.0, stream=False
    )
    return response.choices[0].message.content

def generate_full_path(graph: Graph, query_content: str) -> List[int]:
    """
    Traverse the graph starting at the start_node and ending at the end_node.
    Use the `pick_next_node` function to decide the next step at each node.

    :param graph: The Graph object representing the action graph.
    :param query_content: The query content guiding the traversal.
    :return: A list of node IDs representing the full path from start to end.
    """
    path = []
    visited = set()

    # Start at the start_node
    current_node = graph.get_start_node()
    path.append(current_node.node_id)
    visited.add(current_node.node_id)

    print(f"Starting traversal from start_node: {current_node.node_id}")

    while current_node.node_id != graph.end_node:
        # Get the next nodes from the adjacency list
        next_nodes = [
            {
                "node_id": neighbor.node_id,
                "content": neighbor.content
            }
            for neighbor in graph.get_neighbors(current_node.node_id)
        ]

        # If there are no more neighbors, stop
        if not next_nodes:
            print(f"No further steps available from node {current_node.node_id}. Ending traversal.")
            break

        # Use `pick_next_node` to select the next step
        next_node_id = pick_next_node(
            current_node.content, next_nodes, query_content
        )

        # Find the corresponding node object
        next_node = graph.nodes.get(int(next_node_id))

        if not next_node or next_node.node_id in visited:
            print(f"Stopping traversal. Next node: {next_node_id} | Visited: {visited}")
            break

        # Update path and visited
        path.append(next_node.node_id)
        visited.add(next_node.node_id)
        current_node = next_node

        print(f"Moved to node: {current_node.node_id}")

    print(f"Traversal complete. Path: {path}")
    return path
