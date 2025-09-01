# %%
import io
import re
import json
import gzip
import urllib.request

JOUYOU_URL = "https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji"
KRAD_URL = "http://ftp.edrdg.org/pub/Nihongo/kradfile-u.gz"

# %%

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

request = urllib.request.Request(JOUYOU_URL, headers=headers)

with urllib.request.urlopen(request) as response:
    html = response.read().decode("utf-8")

# %%

with urllib.request.urlopen(KRAD_URL) as response:
    gzipped_file = io.BytesIO(response.read())
    with gzip.open(gzipped_file, "rt") as f:
        krad_lines = f.readlines()

# %%

with open("jlpt.json", encoding="utf-8") as f:
    jlpt_kanjis = json.load(f)

# %%

kanji_levels = {}
for level, kanjis in jlpt_kanjis.items():
    for kanji in kanjis:
        kanji_levels[kanji] = level

# %%

jouyou = {}
for tr in re.findall(r"<tr>\n(.+?)</tr>", html, re.DOTALL):

    tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.DOTALL)

    kanji = tds[1].split("wikt:")[1][0]
    radical = tds[3][-5]
    strokes = int(tds[4])
    # grade = tds[5]
    meanings = tds[7]
    readings = tds[8].split("<br")[0].split("、")

    if kanji == "𠮟":
        kanji = "叱"

    assert kanji not in jouyou, tr

    jlpt = kanji_levels[kanji]

    jouyou[kanji] = {
        "radical": radical,
        "decomp": kanji,
        "meanings": meanings,
        "readings": readings,
        "strokes": int(strokes),
        "jlpt": jlpt,
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

with open("jouyou.json", "w", encoding="utf-8") as f:
    json.dump(jouyou, f, indent=4, ensure_ascii=False)

# %%
