import json

 
with open("kanjis.json", encoding="utf-8") as f:
    kanjis = json.load(f)

with open("jouyou.json", encoding="utf-8") as f:
    jouyou = json.load(f)


def split_on_kun(readings):
    ons = []
    kuns = []
    for reading in readings:
        if reading[0] < '\u30A0': # start of katakana block
            kuns.append(reading)
        else:
            ons.append(reading)
    return ons, kuns

jlpt_entries = {k: [d["meanings"], *split_on_kun(d["readings"])] for k, d in jouyou.items()}

jlpt_kanjis = {}
for level, level_kanjis in kanjis.items():
    jlpt_kanjis[level] = {k: jlpt_entries[k] for k in level_kanjis}

with open("jlpt.json", "w", encoding="utf-8") as f:
    json.dump(jlpt_kanjis, f, indent=4, ensure_ascii=False)

with open("edict.json", encoding="utf-8") as f:
    edict = json.load(f)

for level, kanjis in jlpt_kanjis.items():
    for kanji in kanjis:
        jouyou[kanji]["jlpt"] = level

exclude_tags = ["(uk)", "(abbr)", "(dated)", "(hist)"]

pairs = {f"N{i}": {} for i in reversed(range(1, 6))}

for word, entry in edict.items():
    if len(word) != 2:
        continue
    info0 = jouyou.get(word[0])
    info1 = jouyou.get(word[1])
    if info0 is None or info1 is None:
        continue
    meaning = entry[0][1][1]
    if any(t in meaning for t in exclude_tags):
        continue
    reading = entry[0][0]
    min_jlpt = min(info0["jlpt"], info1["jlpt"])
    pairs[min_jlpt][word] = [reading] + meaning.split("; ")

with open("pairs.json", "w", encoding="utf-8") as f:
    json.dump(pairs, f, indent=4, ensure_ascii=False)

