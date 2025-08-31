# %%
import json

# %%

with open("jouyou.json", encoding="utf-8") as f:
    jouyou = json.load(f)

with open("edict.json", encoding="utf-8") as f:
    edict = json.load(f)

# %%

pairs = {i: {} for i in reversed(range(1, 6))}

for word, entry in edict.items():
    if len(word) != 2:
        continue
    info0 = jouyou.get(word[0])
    info1 = jouyou.get(word[1])
    if info0 is None or info1 is None:
        continue
    meaning = entry[0][1][1]
    if "(uk)" in meaning or "(abbr)" in meaning:
        continue
    min_jlpt = min(info0["jlpt"], info1["jlpt"])
    pairs[min_jlpt][word] = meaning.split("; ")[0]

# %%

pairs = {f"N{i}": l for i, l in pairs.items()}

# %%

with open("pairs.json", "w", encoding="utf-8") as f:
    json.dump(pairs, f, indent=4, ensure_ascii=False)

# %%
