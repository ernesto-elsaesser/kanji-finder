# %%
import io
import csv
import json
import gzip
import urllib.request

JOUYOU_URL = "https://raw.githubusercontent.com/NHV33/joyo-kanji-compilation/refs/heads/master/joyo.csv"

# %%
with urllib.request.urlopen(JOUYOU_URL) as response:
    csv_lines = response.read().decode("utf-8").splitlines()
    reader = csv.reader(csv_lines)
    next(reader)
    jouyou = {r[1]: r[3:] for r in reader}

# %%

with open("edict.json") as f:
    edict = json.load(f)

# %%

pairs = {k: v for k, v in edict.items()
          if len(k) == 2 and k[0] in jouyou and k[1] in jouyou}

# %%

with open("pairs.json", "w") as f:
    json.dump(pairs, f, indent=4, ensure_ascii=False)

# %%
