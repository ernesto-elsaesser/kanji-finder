# %%
import io
import json
import gzip
import urllib.request

EDICT_URL = "http://ftp.edrdg.org/pub/Nihongo/edict2u.gz"

# %%
with urllib.request.urlopen(EDICT_URL) as response:
    gzipped_file = io.BytesIO(response.read())
    with gzip.open(gzipped_file, "rt") as f:
        lines = f.readlines()

# %%

rows = [l[:-2].split("/") for l in lines[1:]]

# %%

edict = {r[0]: "; ".join(r[1:-3])
         for r in rows if r[-2] == "(P)" and "[" in r[0]}

# %%

sorted_keys = sorted(edict, key=lambda k: k.index("["))
edict = {k: edict[k] for k in sorted_keys}

# %%

with open("edict.json", "w") as f:
    json.dump(edict, f, indent=1, ensure_ascii=False)

# %%
