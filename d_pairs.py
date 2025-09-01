# %%
import re
import json
import urllib.request

JOUYOU_URL = "https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji"

# %%

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

request = urllib.request.Request(JOUYOU_URL, headers=headers)

with urllib.request.urlopen(request) as response:
    html = response.read().decode("utf-8")

# %%

jouyou = {}
grades = []
for tr in re.findall(r"<tr>\n(.+?)</tr>", html, re.DOTALL):

    tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.DOTALL)

    kanji = tds[1].split("wikt:")[1][0]
    radical = tds[3][-5]
    strokes = int(tds[4])
    grade = int(tds[5].replace("S", "7"))
    meanings = tds[7]
    readings = tds[8].split("<br")[0].split("、")

    if kanji == "𠮟":
        kanji = "叱"

    assert kanji not in jouyou, tr

    jouyou[kanji] = {
        "radical": radical,
        "decomp": kanji,
        "meanings": meanings,
        "readings": readings,
        "strokes": int(strokes),
    }

    grades.append((grade, kanji))

# %%

jouyou = {k: jouyou[k] for _, k in sorted(grades)}

# %%

with open("jouyou.json", "w", encoding="utf-8") as f:
    json.dump(jouyou, f, indent=4, ensure_ascii=False)

# %%

with open("jlpt.json", encoding="utf-8") as f:
    jlpt_kanjis = json.load(f)

with open("edict.json", encoding="utf-8") as f:
    edict = json.load(f)

# %%

for level, kanjis in jlpt_kanjis.items():
    for kanji in kanjis:
        jouyou[kanji]["jlpt"] = level

# %%

pairs = {f"N{i}": {} for i in reversed(range(1, 6))}

for word, entry in edict.items():
    if len(word) != 2:
        continue
    info0 = jouyou.get(word[0])
    info1 = jouyou.get(word[1])
    if info0 is None or info1 is None:
        continue
    meaning = entry[0][1][1]
    if "(uk)" in meaning or "(abbr)" in meaning or "(dated)" in meaning:
        continue
    reading = entry[0][0]
    min_jlpt = min(info0["jlpt"], info1["jlpt"])
    pairs[min_jlpt][word] = [reading] + meaning.split("; ")

# %%

with open("pairs.json", "w", encoding="utf-8") as f:
    json.dump(pairs, f, indent=4, ensure_ascii=False)

# %%
