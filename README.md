# GraphThought

Implementation of GraphThought: a reasoning framework for LLMs based on dynamic DAG construction, reformulating inference as a directed acyclic graph instead of a linear chain.

Companion code for the independent research preprint "GraphThought: Structured Multi-Path Reasoning via Dynamic Computation Graphs in Large Language Models."

## How it works

[NODE 1] Identify relevant Proms season -> 1945
[NODE 2|dep:1] Opening concert -> Sept 14, 1945
[NODE 3|dep:2] Work performed -> Beethoven's 9th
[NODE 4|dep:3] Composer -> Beethoven
[NODE 5|dep:4] Birth year -> 1770
[ANSWER|dep:5] 1770

## Setup

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY=your_key

## Quick start

from graphthought.planner import plan
from graphthought.executor import run

question = "What river flows through the city where the Eiffel Tower is located?"
graph = plan(question)
_, answer = run(question, graph)
print(answer)

## Reproduce HotpotQA evaluation

python evaluation/run_eval.py

Results accumulate in data/hotpotqa_results.csv. The script resumes automatically if interrupted by API rate limits.

## Repository structure

graphthought/        Core library
  graph_parser.py    GSF parser, cycle detection, topological sort
  planner.py         Phase 1: graph skeleton generation
  executor.py        Phase 2: sequential/parallel node resolution
  prompts/           System prompts for planning and node resolution
evaluation/          Evaluation scripts
examples/            Worked examples on HotpotQA
data/                Evaluation results (CSV)

## Notes

This is an independent research project, evaluated using Google Gemini 2.5 Flash (free tier) due to API budget constraints. Results in the companion paper are reported separately and should be read alongside this implementation rather than treated as identical reproductions, since model choice affects absolute accuracy.
