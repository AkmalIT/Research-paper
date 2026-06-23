import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from graphthought.planner import plan
from graphthought.executor import run

questions = [
    "What river flows through the city where the Eiffel Tower is located?",
    "Who was the president of the United States when the Berlin Wall fell?",
    "What is the capital of the country where the Amazon river originates?",
]

for q in questions:
    print(f"\nQ: {q}")
    graph = plan(q)
    print(f"   Nodes: {len(graph.nodes)} | Valid: {graph.is_valid}")
    _, answer = run(q, graph)
    print(f"   A: {answer}")
