import subprocess
import time
import sys
import os

# работаем относительно папки, где лежит этот bench.py
HERE = os.path.dirname(os.path.abspath(__file__))
A_PY = os.path.join(HERE, "a.py")
INP  = os.path.join(HERE, "bench_input.txt")
OUT  = os.path.join(HERE, "bench_output.txt")

sizes = [1000, 5000, 10000, 50000, 100000]

print(f"{'n':>8} {'время (мс)':>12}")
print("-" * 22)

results = []
for n in sizes:
    # генерируем сбалансированный журнал
    with open(INP, "w", encoding="utf-8") as f:
        for i in range(n):
            f.write(f"LOGIN u{i}\n")
            f.write(f"LOGOUT u{i}\n")

    start = time.perf_counter()
    r = subprocess.run(
        [sys.executable, A_PY, INP, OUT],
        capture_output=True, text=True
    )
    elapsed_ms = (time.perf_counter() - start) * 1000

    if r.returncode != 0:
        print(f"a.py упал на n={n}")
        print("STDOUT:", r.stdout)
        print("STDERR:", r.stderr)
        sys.exit(1)

    results.append((n, elapsed_ms))
    print(f"{n:>8} {elapsed_ms:>12.2f}")

# сохранить в файл для отчёта
with open(os.path.join(HERE, "bench_results.txt"), "w", encoding="utf-8") as f:
    f.write("n\tвремя_мс\n")
    for n, t in results:
        f.write(f"{n}\t{t:.2f}\n")

print("\nГотово. Результаты в bench_results.txt")