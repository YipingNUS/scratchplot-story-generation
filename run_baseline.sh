#!/usr/bin/env bash

python3 dino.py \
 --output_dir movie_exp \
 --task_file movie_task_specs/plot-baseline.json \
 --num_entries_per_label 50 \
 --min_num_tokens 100 \
 --max_output_length 150 \
 --top_k 30 \
 --keep_outputs_without_eos \
 --allow_newlines_in_outputs \
 --batch_size 10 \
 --ignore_eos


