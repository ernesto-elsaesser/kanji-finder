# %%
import json

# %%

with open("jouyou.json") as f:
    jouyou = json.load(f)

with open("edict.json") as f:
    edict = json.load(f)

# %%

pairs = {i: [] for i in reversed(range(1, 6))}

for word in edict:
    if len(word) != 2:
        continue
    info0 = jouyou.get(word[0])
    info1 = jouyou.get(word[1])
    if info0 is None or info1 is None:
        continue
    min_jlpt = min(info0["jlpt"], info1["jlpt"])
    pairs[min_jlpt].append(word)

# %%

pairs = {f"N{i}": l for i, l in pairs.items()}

# %%

with open("pairs.json", "w") as f:
    json.dump(pairs, f, indent=4, ensure_ascii=False)

# %%
