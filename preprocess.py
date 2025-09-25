from pathlib import Path
import json, random
from utils import normalize_urdu, normalize_roman

# Point to the dataset root (the one that has poet folders like faiz-ahmad-faiz, allama-iqbal, etc.)
root = Path("urdu_ghazals_rekhta/dataset/extracted/dataset")
pairs = []

print("Root path:", root.resolve())
print("Sample poet dirs:", [p.name for p in root.iterdir() if p.is_dir()][:5])

for poet in root.iterdir():
    if not poet.is_dir():
        continue
    ur_path = poet / "ur"
    en_path = poet / "en"
    if not ur_path.exists() or not en_path.exists():
        continue

    # iterate over *all files*, not just .txt
    for ur_file in ur_path.iterdir():
        if not ur_file.is_file():
            continue
        en_file = en_path / ur_file.name
        if not en_file.exists():
            continue

        ur_lines = ur_file.read_text(encoding="utf8").splitlines()
        en_lines = en_file.read_text(encoding="utf8").splitlines()

        for u, e in zip(ur_lines, en_lines):
            u, e = normalize_urdu(u.strip()), normalize_roman(e.strip())
            if u and e:
                pairs.append([u, e])

print("Total aligned pairs collected:", len(pairs))
print("Example pairs:", pairs[:5])

# Shuffle + split
random.seed(42)
random.shuffle(pairs)
n = len(pairs)
splits = {
    "train": pairs[:int(0.5*n)],
    "val": pairs[int(0.5*n):int(0.75*n)],
    "test": pairs[int(0.75*n):]
}

Path("data").mkdir(exist_ok=True)
for k, v in splits.items():
    out_path = Path("data") / f"{k}.json"
    json.dump(v, open(out_path, "w", encoding="utf8"), ensure_ascii=False, indent=2)
    print(f"{k} size:", len(v))
