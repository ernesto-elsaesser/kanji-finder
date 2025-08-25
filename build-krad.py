# %%
import io
import csv
import json
import gzip
import urllib.request

KRAD_URL = "https://github.com/neocl/jamdict/raw/refs/heads/main/jamdict/data/kradfile-u.gz"
JOYO_URL = "https://raw.githubusercontent.com/NHV33/joyo-kanji-compilation/refs/heads/master/joyo.csv"

# %%
with urllib.request.urlopen(JOYO_URL) as response:
    csv_lines = response.read().decode("utf-8").splitlines()
    reader = csv.reader(csv_lines)
    next(reader)
    jouyou = {r[1] for r in reader}

# %%
with urllib.request.urlopen(KRAD_URL) as response:
    gzipped_file = io.BytesIO(response.read())
    with gzip.open(gzipped_file, "rt") as f:
        lines = f.readlines()

# %%

lines = [l[:-1] for l in lines if l[0] != "#"]

# %%

lines = [l for l in lines if l[0] in jouyou]

# %%

lines = sorted(lines, key=len)

# %%
krad = {l[0]: l[4:].replace(" ", "") for l in lines}
krad = {k: v for k, v in krad.items() if k != v}

# %%

with open("krad.json", "w") as f:
    json.dump(krad, f, indent=4, ensure_ascii=False)

# %%
