import subprocess, sys


def one_run(rid, ckpt, kill_at=None, park=None):
    args = [sys.executable, "agent.py", rid, ckpt or "-"]
    if park is not None:
        args.append(str(park))
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
    first, seen = None, 0
    for line in iter(p.stdout.readline, ""):
        if line.startswith("TOOL_RESULT"):
            seen += 1
            first = first if first is not None else int(line.split()[1])
        if line.startswith("WINDOW_OPEN") or seen == kill_at:
            p.kill()
            break
    p.wait()
    return first


def arm(prefix, use_ckpt, park=None, n=100):
    at = {}
    for i in range(n):
        rid = f"{prefix}-{i}"
        ckpt = f"ckpt-{rid}.json" if use_ckpt else None
        one_run(rid, ckpt, kill_at=3 if park is None else None, park=park)
        first = one_run(rid, ckpt)
        at[first] = at.get(first, 0) + 1
    print(f"{prefix}: resumed at {dict(sorted(at.items()))}", flush=True)


if __name__ == "__main__":
    arm("baseline", False)
    arm("race", True)
    arm("window", True, park=2)