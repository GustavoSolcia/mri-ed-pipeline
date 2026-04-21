#!/bin/bash

VALID_ARGS=$(getopt -o s:p: --long sequence:,phantom: -- "$@")
if [[ $? -ne 0 ]]; then
    exit 1;
fi

eval set -- "$VALID_ARGS"
while [ : ]; do
  case "$1" in
    -s | --sequence)
        SEQ=$2
        shift 2
        ;;
    -p | --phantom)
        PHANTOM=$2
        shift 2
        ;;
    ?|h)
      echo "Usage: $(basename $0) [-s | --sequence <sequence_name>]"
      exit 1
      ;;
    --) shift; 
        break 
        ;;
  esac
done

# Making sure all data and figure folders exists
# in case that the repository was cloned.
mkdir -p data/nii
mkdir -p data/phantom
mkdir -p data/sequence
mkdir -p data/simulation
mkdir -p figures/pdf
mkdir -p figures/svg

# Creates the phantom if you don't have it
if [ "$PHANTOM" = "water_spheres" ]; then
    if [ ! -f data/phantom/water_spheres.phantom ]; then
        echo "Creating phantom..."
        julia --project=. src/phantom/make_water_spheres.jl
    fi
fi

echo "Writing sequence..."
python3 src/write_sequence.py --sequence $SEQ

echo "Running simulation..."
julia --project=. src/simulate.jl \
    data/phantom/water_spheres.phantom \
    data/sequence/$SEQ.seq \
    data/simulation/$SEQ.mat \
    $SEQ \
    $PHANTOM

echo "Running post-processing..."
python3 src/post_process.py --sequence $SEQ --phantom $PHANTOM
