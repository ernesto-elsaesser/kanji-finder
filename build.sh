echo "jouyou.json ..."
python3 load_jouyou.py jouyou.json
echo "edict.json ..."
python3 load_edict.py radicals/edict.json
echo "krad.json ..."
python3 load_krad.py jouyou.json radicals/krad.json
echo "pairs.json ..."
python3 build_quiz.py jouyou.json radicals/edict.json quiz/jlpt.json quiz/pairs.json
