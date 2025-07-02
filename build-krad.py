# https://github.com/neocl/jamdict/blob/main/jamdict/data/kradfile-u.gz

import json

with open("edict2.json") as f:
    edict = json.load(f)

edict_index = {k for e in edict for k in e}

with open("kradfile-u") as f:
    lines = [l[:-1] for l in f if l[0] != "#"]

lines = sorted(lines, key=len)
krad = {l[0]: l[4:].replace(" ", "") for l in lines if l[0] in edict_index}
krad = {k: v for k, v in krad.items() if k != v}

with open("krad.json", "w") as f:
    json.dump(krad, f, indent=4, ensure_ascii=False)
