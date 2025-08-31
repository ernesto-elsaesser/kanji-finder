# %%
import json

# %%

with open("jouyou.json") as f:
    jouyou = json.load(f)

with open("edict.json") as f:
    edict = json.load(f)

# %%

pairs = {k: v for k, v in edict.items()
          if len(k) == 2 and k[0] in jouyou and k[1] in jouyou}

# %%

with open("pairs.json", "w") as f:
    json.dump(pairs, f, indent=4, ensure_ascii=False)

# %%
