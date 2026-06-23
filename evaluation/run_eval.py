import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from datasets import load_dataset
from tqdm import tqdm
from graphthought.planner import plan
from graphthought.executor import run

def exact_match(pred, gold):
    return pred.strip().lower() == gold.strip().lower()

def evaluate(n_samples=6, model="gemini-2.5-flash"):
    dataset = load_dataset("hotpotqa/hotpot_qa", "distractor", split="validation")

    csv_path = "data/hotpotqa_results.csv"
    os.makedirs("data", exist_ok=True)

    if os.path.exists(csv_path):
        existing = pd.read_csv(csv_path)
        start = len(existing)
        print(f"Продолжаем с примера {start}, уже сделано: {start}")
    else:
        existing = pd.DataFrame()
        start = 0

    samples = list(dataset.select(range(start, start + n_samples)))

    for item in tqdm(samples, desc="Evaluating"):
        question = item["question"]
        gold = item["answer"]

        try:
            graph = plan(question, model)
            _, prediction = run(question, graph, model)
        except Exception as e:
            print(f"\nОшибка: {e}")
            print("Сохраняю прогресс и останавливаюсь.")
            break

        is_correct = exact_match(prediction, gold)
        row = pd.DataFrame([{
            "question": question,
            "gold": gold,
            "prediction": prediction,
            "correct": is_correct,
            "n_nodes": len(graph.nodes),
            "valid_graph": graph.is_valid,
        }])

        # Сохраняем сразу после каждого примера
        existing = pd.concat([existing, row], ignore_index=True)
        existing.to_csv(csv_path, index=False)

    total = len(existing)
    if total > 0:
        total_correct = existing["correct"].sum()
        print(f"\nВсего сделано: {total}/30")
        print(f"Accuracy: {total_correct}/{total} = {total_correct/total*100:.1f}%")
        print(f"Avg nodes: {existing['n_nodes'].mean():.1f}")

if __name__ == "__main__":
    evaluate()
