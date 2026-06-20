#!/usr/bin/env bash
set -u
GM=/tmp/genmorph_pilot/genmorph_full/genmorph; cd "$GM"
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64; export PATH="$JAVA_HOME/bin:/opt/maven/bin:$PATH"
CFG=configs/config-all-evaluation-math-gcd.json
for SEED in 11 12 13 21 22 23 31 32 33 41 42 43; do
  echo "############ SEED $SEED $(date +%H:%M:%S) ############"
  python3 - "$SEED" <<'PY'
import json,sys; s=int(sys.argv[1]); p="configs/config-all-evaluation-math-gcd.json"
c=json.load(open(p)); c['experiment-config-override']['@']['generation_seeds']=[s]; c['runs']=[{'seed':s}]
json.dump(c,open(p,'w'),indent=1)
PY
  SRC="output_dir_math/evaluation_test_inputs_seed$SEED/MathClass?gcd?0"
  if ! ls "$SRC"/*.methodinputs >/dev/null 2>&1; then
    rm -rf "output_dir_math/evaluation_test_inputs_seed$SEED" "output_dir_math/randoop_seed$SEED" 2>/dev/null
    timeout 260 python3 scripts/run/genmorph.py eval "$CFG" > /tmp/gen_$SEED.log 2>&1
  fi
  n=$(ls "$SRC"/*.methodinputs 2>/dev/null | wc -l); echo "  source=$n"
  timeout 400 python3 /tmp/setn_eval.py "MathClass?gcd?0" "$SEED" > /tmp/setn_$SEED.log 2>&1
  echo "  $(grep -E 'DONE|FATAL' /tmp/setn_$SEED.log | head -1 || echo FAILED)"
done
echo "ALL DONE $(date +%H:%M:%S)"
