# jouyou table from https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji
# alternative: https://www.kaggle.com/datasets/anthaus/japanese-jy-kanji
echo "edict.json ..."
python3 1_load_edict.py
echo "krad.json ..."
python3 2_load_krad.py
echo "pairs.json ..."
python3 3_build_quiz.py
