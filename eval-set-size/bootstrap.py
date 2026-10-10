import json
import numpy as np
import matplotlib.pyplot as plt

correct = np.array(
    [json.loads(line)["correct"] for line in open("results.jsonl")], dtype=float
)
SIZES, DRAWS = [10, 20, 25, 50, 100, 200], 30
rng = np.random.default_rng(0)

scores = {
    n: rng.choice(correct, size=(DRAWS, n), replace=True).mean(axis=1) for n in SIZES
}
for n, s in scores.items():
    perfect = int((s == 1.0).sum())
    print(
        f"n={n:>3} | perfect in {perfect:>2}/{DRAWS} draws | perfect only proves failures < {3 / n:.1%}"
    )


true_fail = (1 - correct.mean()) * 100
n_axis = np.arange(10, 501)
plt.style.use("dark_background")
plt.plot(
    n_axis,
    300 / n_axis,
    color="#007BFF",
    label="what a perfect score proves: failures < 3/n",
)
plt.scatter(SIZES, [300 / n for n in SIZES], color="#007BFF", s=30)
plt.axhline(
    true_fail,
    color="white",
    linestyle="--",
    label=f"this agent's real failure rate: {true_fail:.2f}%",
)
plt.yscale("log")
plt.yticks([0.5, 1, 3, 10, 30], ["0.5%", "1%", "3%", "10%", "30%"])
plt.minorticks_off()
plt.xlabel("eval set size (cases, all passing)")
plt.ylabel("failure rate")
plt.title("What a perfect score actually proves")
plt.legend()
plt.savefig("spread.png", dpi=150)
plt.show()
