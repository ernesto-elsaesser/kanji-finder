# %%
import io
import re
import json
import gzip
import urllib.request

EDICT_URL = "http://ftp.edrdg.org/pub/Nihongo/edict_sub.gz"

# %%
with urllib.request.urlopen(EDICT_URL) as response:
    gzipped_file = io.BytesIO(response.read())
    with gzip.open(gzipped_file, "rt", encoding="EUC-JP") as f:
        lines = f.readlines()

# %%

multi_entry_regex = re.compile(r"\(([a-z0-9,-]+)\) \([0-9]\) (.+)")
single_entry_regex = re.compile(r"\(([a-z0-9,-]+)\) (.+)")

edict = {}
for line in lines[1:]:
    if "(gikun)" in line or "(ateji)" in line:
        continue

    if line.endswith("/(P)/\n"):
        line = line[:-6]
    else:
        line = line[:-2]
        print("(P) in meaning in: " + line)

    if "(sK)" in line:
        print("(sK) tag in: " + line)
        line = line.replace("(sK) ", "")

    row = line.split("/")
    if "[" not in row[0]:
        continue  # no kanji
    word, reading = row[0][:-2].split(" [")

    entry: list = [reading]
    for term in row[1:]:
        match = multi_entry_regex.match(term)
        if match is None:
            match = single_entry_regex.match(term)
        if match is None:
            assert len(entry) > 1, line
            entry[-1][1] += "; " + term
        else:
            pos = match.group(1)
            meaning = match.group(2)
            entry.append([pos, meaning])

    if word in edict:
        edict[word].append(entry)
    else:
        edict[word] = [entry]

# %%

sorted_keys = sorted(edict)
sorted_keys = sorted(sorted_keys, key=lambda k: len(k))
edict = {k: edict[k] for k in sorted_keys}

# %%

with open("edict.json", "w", encoding="utf-8") as f:
    json.dump(edict, f, indent=1, ensure_ascii=False)

# %%
