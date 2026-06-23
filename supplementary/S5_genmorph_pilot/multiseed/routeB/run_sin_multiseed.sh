#!/usr/bin/env bash
set -u
GM=/tmp/genmorph_pilot/genmorph_full/genmorph; cd "$GM"
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64; export PATH="$JAVA_HOME/bin:/opt/maven/bin:$PATH"
# sin-only configs
python3 - <<'PY'
import json
d=json.load(open('configs/sut-config-math.json')); d['suts']['MathClass']={'sin':[0]}
json.dump(d,open('configs/sut-config-math-sin.json','w'),indent=1)
c=json.load(open('configs/config-all-evaluation-math.json'))
c['sut-config']='configs/sut-config-math-sin.json'
c['experiment-config-override']['@'].setdefault('randoop',{})['num_executions']=1
c['experiment-config-override']['@']['randoop']['time_budget_seconds']=120
json.dump(c,open('configs/config-all-evaluation-math-sin.json','w'),indent=1)
print("sin configs written")
PY
CFG=configs/config-all-evaluation-math-sin.json
for SEED in 11 12 13 21 22 23 31 32 33 41 42 43; do
  echo "############ SIN SEED $SEED $(date +%H:%M:%S) ############"
  python3 - "$SEED" <<'PY'
import json,sys; s=int(sys.argv[1]); p="configs/config-all-evaluation-math-sin.json"
c=json.load(open(p)); c['experiment-config-override']['@']['generation_seeds']=[s]; c['runs']=[{'seed':s}]
json.dump(c,open(p,'w'),indent=1)
PY
  SRC="output_dir_math/evaluation_test_inputs_seed$SEED/MathClass?sin?0"
  if ! ls "$SRC"/*.methodinputs >/dev/null 2>&1; then
    timeout 260 python3 scripts/run/genmorph.py eval "$CFG" > /tmp/gensin_$SEED.log 2>&1
  fi
  n=$(ls "$SRC"/*.methodinputs 2>/dev/null | wc -l); echo "  source=$n"
  timeout 400 python3 /tmp/setn_eval2.py "MathClass?sin?0" "$SEED" > /tmp/setnsin_$SEED.log 2>&1
  echo "  $(grep -E 'DONE|FATAL|Error' /tmp/setnsin_$SEED.log | head -1 || echo FAILED)"
done
echo "ALL SIN DONE $(date +%H:%M:%S)"
