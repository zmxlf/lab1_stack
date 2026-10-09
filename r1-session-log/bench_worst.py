import subprocess
import time
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A_PY = os.path.join(HERE, "a.py")

def generate_normal(path, n):
    with open(path, "w", encoding="utf-8") as f:
        for i in range(n):
            f.write(f"LOGIN u{i}\n")
            f.write(f"LOGOUT u{i}\n")

def generate_worst(path, n):
    with open(path, "w", encoding="utf-8") as f:
        for i in range(n):
            f.write(f"LOGIN u{i}\n")

def measure(inp, out):
    start = time.perf_counter()
    subprocess.run([sys.executable, A_PY, inp, out], capture_output=True)
    return (time.perf_counter() - start) * 1000

sizes = [10000, 50000, 100000]

print(f"{'n':>8} {'обычный, мс':>14} {'худший, мс':>14} {'отношение':>12}")
print("-" * 52)

for n in sizes:
    generate_normal("n_in.txt", n)
    t_norm = measure("n_in.txt", "n_out.txt")

    generate_worst("w_in.txt", n)
    t_worst = measure("w_in.txt", "w_out.txt")

    ratio = t_worst / t_norm
    print(f"{n:>8} {t_norm:>14.2f} {t_worst:>14.2f} {ratio:>12.2f}")