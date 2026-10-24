#!/bin/bash

set -euo pipefail

usage() {
 echo "Usage: $(basename "$0") -e|--experiment <experiment_name> -r|--run <run_name>" \
      "[-b|--backend <cpu|gpu>] [-t|--threads <n>]"
}

EXP=""
RUN=""
BACKEND="cpu"
THREADS="$(nproc 2>/dev/null || echo 4)"

VALID_ARGS=$(getopt -o e:r:b:t:h --long experiment:,run:,backend:,threads:,help -- "$@")
if [[ $? -ne 0 ]]; then
    usage
    exit 1;
fi

eval set -- "$VALID_ARGS"
while [ : ]; do
    case "$1" in
        -e | --experiment)
         EXP=$2
         shift 2
         ;;
        -r | --run)
         RUN=$2
         shift 2
         ;;
        -b | --backend)
         BACKEND=$2
         shift 2
         ;;
        -t | --threads)
         THREADS=$2
         shift 2
         ;;
        -h | --help)
         usage
         exit 0
         ;;
        --) shift;
         break
         ;;
        *)
         usage
         exit 1
         ;;
    esac
done

if [[ -z "$EXP" || -z "$RUN" ]]; then
    echo "Error: --experiment and --run are required."
    usage
    exit 1
fi

CONFIG="experiments/$EXP/$RUN.yml"
if [[ ! -f "$CONFIG" ]]; then
    echo "Error: configuration file not found: $CONFIG"
    exit 1
fi

export PYTHON_JULIACALL_THREADS="$THREADS"
[[ "$THREADS" -gt 1 ]] && export PYTHON_JULIACALL_HANDLE_SIGNALS=yes

echo "Running simulation experiment..."
python3 src/run_simulation.py \
 --experiment "$EXP" --run "$RUN" \
 --backend "$BACKEND" --threads "$THREADS"
