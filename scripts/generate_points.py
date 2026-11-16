"""Reproduce the coordinates of the author's original 600-point comparison."""
import json
import random
from pathlib import Path

rng = random.Random(2026110302)
n, side, margin, distance = 1200, 1000, 3, 19
b = [(rng.uniform(margin, side-margin), rng.uniform(margin, side-margin)) for _ in range(n)]
a, buckets = [], {}
for attempt in range(1000000):
    x, y = rng.uniform(margin, side-margin), rng.uniform(margin, side-margin)
    kx, ky = int(x/distance), int(y/distance)
    if any((x-px)**2+(y-py)**2 < distance**2
           for i in range(kx-1, kx+2) for j in range(ky-1, ky+2)
           for px, py in buckets.get((i, j), [])):
        continue
    a.append((x, y))
    buckets.setdefault((kx, ky), []).append((x, y))
    if len(a) == n:
        break
assert len(a) == n
a, b = a[::2], b[::2]
assert len(a) == len(b) == 600
assert min((x-u)**2+(y-v)**2 for i, (x, y) in enumerate(a) for u, v in a[i+1:]) >= 19**2
destination = Path(__file__).resolve().parents[1] / 'points.json'
destination.write_text(json.dumps({'a': a, 'b': b}, separators=(',', ':')), encoding='utf-8')
print('Generated original coordinates: A=600, B=600; minimum A separation verified.')
