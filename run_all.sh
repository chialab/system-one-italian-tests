#!/bin/sh
# Usage: ./run_all.sh <systemone url> <model name> <results tag>
set -e
URL=$1
MODEL=$2
TAG=$3
DIR=results/$TAG
cd "$(dirname "$0")"
mkdir -p "$DIR"
python3 suite_run.py --url "$URL" --model "$MODEL" --tag "$TAG" --data suite_data --langs it,en 2>&1 | tee "$DIR/suite_data_it-en.log"
python3 suite_run.py --url "$URL" --model "$MODEL" --tag "$TAG" --data suite_data_hard --langs it 2>&1 | tee "$DIR/suite_data_hard_it.log"
python3 pilot_12_cases.py "$URL" "$DIR/pilot_12_cases_it-en.json" "$MODEL" 2>&1 | tee "$DIR/pilot_12_cases_it-en.log"
python3 pilot_latency.py "$URL" - "$MODEL" 2>&1 | tee "$DIR/pilot_latency_it.log"
echo "ALL_DONE $TAG"
