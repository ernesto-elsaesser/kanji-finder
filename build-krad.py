# %%
import io
import csv
import json
import gzip
import urllib.request

KRAD_URL = "http://ftp.edrdg.org/pub/Nihongo/kradfile-u.gz"
JOUYOU_URL = "https://raw.githubusercontent.com/NHV33/joyo-kanji-compilation/refs/heads/master/joyo.csv"

# %%
with urllib.request.urlopen(JOUYOU_URL) as response:
    csv_lines = response.read().decode("utf-8").splitlines()
    reader = csv.reader(csv_lines)
    next(reader)
    jouyou = {r[1]: r[3:] for r in reader}

# %%
with urllib.request.urlopen(KRAD_URL) as response:
    gzipped_file = io.BytesIO(response.read())
    with gzip.open(gzipped_file, "rt") as f:
        lines = f.readlines()

# %%

entries = []
for line in lines:
    kanji = line[0]
    if kanji == "#": # comment line
        continue

    decomp = line[4:-1].replace(" ", "")
    if decomp == kanji:
        continue

    info = jouyou.get(kanji)
    if info is None:
        continue

    radical, strokes, grade, year, meanings, on, kun, freq, jlpt = info
    entry = {
        "decomp": decomp,
        "radical": radical,
        "meanings": meanings,
        "on": on.split("|")[0],
        "kun": kun.split("|")[0],
        "strokes": int(strokes),
        "grade": grade,
        "jlpt": int(jlpt),
        "freq": int(freq),
    }
    entries.append((int(freq), kanji, entry))

# %%

krad = {k: e for _, k, e in sorted(entries)}

# %%

with open("krad.json", "w") as f:
    json.dump(krad, f, indent=4, ensure_ascii=False)

# %%
