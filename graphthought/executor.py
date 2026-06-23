from pathlib import Path
from google import genai
from google.genai import types
import os, time
from .graph_parser import ReasoningGraph, topological_layers

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
NODE_PROMPT = (Path(__file__).parent / "prompts" / "node_prompt.txt").read_text()

def _resolve_node(node, resolved, question, model):
    context = "\n".join(
        f"  Node {dep}: {resolved[dep]}"
        for dep in node.dependencies if dep in resolved
    )
    user_content = (
        f"Question: {question}\n\n"
        f"Your task: {node.proposition}\n\n"
        + (f"Established so far:\n{context}\n\n" if context else "")
        + "Resolve this step concisely."
    )
    time.sleep(15)  # free tier: 5 req/min → ждём 13 сек между запросами
    response = client.models.generate_content(
        model=model,
        config=types.GenerateContentConfig(system_instruction=NODE_PROMPT),
        contents=user_content
    )
    return response.text.strip()

def run(question: str, graph: ReasoningGraph, model: str = "gemini-2.5-flash"):
    resolved = {}
    for layer in topological_layers(graph):
        for nid in layer:
            resolved[nid] = _resolve_node(graph.nodes[nid], resolved, question, model)

    sink_ids = [
        nid for nid, node in graph.nodes.items()
        if not any(nid in n.dependencies for n in graph.nodes.values())
    ]
    final = resolved.get(max(sink_ids), graph.answer or "") if sink_ids else (graph.answer or "")
    return resolved, final
