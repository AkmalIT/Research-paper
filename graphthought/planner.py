from pathlib import Path
from google import genai
from google.genai import types
import os
from .graph_parser import parse_gsf, ReasoningGraph

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
PLANNING_PROMPT = (Path(__file__).parent / "prompts" / "planning_prompt.txt").read_text()

def plan(question: str, model: str = "gemini-2.5-flash") -> ReasoningGraph:
    response = client.models.generate_content(
        model=model,
        config=types.GenerateContentConfig(system_instruction=PLANNING_PROMPT),
        contents=f"Question: {question}"
    )
    graph = parse_gsf(response.text)
    if not graph.is_valid or not graph.nodes:
        graph.is_valid = False
    return graph
