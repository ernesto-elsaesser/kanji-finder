# %%
import io
import json
import gzip
import urllib.request

KRAD_URL = "http://ftp.edrdg.org/pub/Nihongo/kradfile-u.gz"

# %%

with urllib.request.urlopen(KRAD_URL) as response:
    gzipped_file = io.BytesIO(response.read())
    with gzip.open(gzipped_file, "rt") as f:
        krad_lines = f.readlines()

# %%

with open("jouyou.json", encoding="utf-8") as f:
    jouyou = json.load(f)

# %%

rows = []
for line in krad_lines:
    kanji = line[0]
    if kanji == "#": # comment line
        continue

    decomp = line[4:-1].replace(" ", "")

    row = [8, len(decomp), kanji, decomp]

    info = jouyou.get(kanji)
    if info is not None:
        row[0] = info["grade"]
        row.append(info["meanings"])

    rows.append(row)

# %%

krad = [r for _, _, *r in sorted(rows)]
# %%

with open("krad.json", "w", encoding="utf-8") as f:
    json.dump(krad, f, indent=4, ensure_ascii=False)

# %%
