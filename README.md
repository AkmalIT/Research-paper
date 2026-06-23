# GraphThought

Implementation of **GraphThought**: a reasoning framework for LLMs based on dynamic DAG construction.

## Setup
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key
```

## Quick start
```python
from openai import OpenAI
from graphthought.planner import plan
from graphthought.executor import run

client = OpenAI()
question = "What river flows through the city where the Eiffel Tower is located?"
graph = plan(question, client)
_, answer = run(question, graph)
print(answer)
```

## Reproduce results
```bash
python evaluation/run_eval.py
```
