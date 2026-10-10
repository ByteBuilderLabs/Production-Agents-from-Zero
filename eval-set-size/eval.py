import argparse, json, random

parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int, default=20)
parser.add_argument("--seed", type=int, default=0)
args = parser.parse_args()

results = [json.loads(line) for line in open("results.jsonl")]
golden_set = random.Random(args.seed).sample(
    results, args.n
)  # no duplicates, like a real golden set
score = sum(r["correct"] for r in golden_set)
print(f"seed {args.seed:>2} | accuracy {score / args.n:.0%} ({score}/{args.n})")
