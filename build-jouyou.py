# %%
import io
import csv
import json
import gzip
import urllib.request

JOUYOU_URL = "https://raw.githubusercontent.com/NHV33/joyo-kanji-compilation/refs/heads/master/joyo.csv"
KRAD_URL = "http://ftp.edrdg.org/pub/Nihongo/kradfile-u.gz"

# %%

with urllib.request.urlopen(JOUYOU_URL) as response:
    csv_lines = response.read().decode("utf-8").splitlines()
    reader = csv.reader(csv_lines)
    next(reader)
    rows = list(reader)

# %%

with urllib.request.urlopen(KRAD_URL) as response:
    gzipped_file = io.BytesIO(response.read())
    with gzip.open(gzipped_file, "rt") as f:
        krad_lines = f.readlines()

# %%

jouyou = {}
for row in rows:

    kanji = row[1]
    radical, strokes, grade, year, meanings, on, kun, freq, jlpt = row[3:]

    jouyou[kanji] = {
        "radical": radical,
        "decomp": kanji,
        "meanings": meanings,
        "on": on.split("|")[0],
        "kun": kun.split("|")[0],
        "strokes": int(strokes),
        "grade": grade,
        "jlpt": int(jlpt),
        "freq": int(freq),
    }

# %%

jlpts = [(v["jlpt"], k) for k, v in jouyou.items()]
jouyou = {k: jouyou[k] for _, k in sorted(jlpts, reverse=True)}

# %%

for line in krad_lines:
    kanji = line[0]
    if kanji == "#": # comment line
        continue

    decomp = line[4:-1].replace(" ", "")
    if decomp == kanji:
        continue

    info = jouyou.get(kanji)
    if info is not None:
        info["decomp"] = decomp


# %%

with open("jouyou.json", "w") as f:
    json.dump(jouyou, f, indent=4, ensure_ascii=False)

# %%
