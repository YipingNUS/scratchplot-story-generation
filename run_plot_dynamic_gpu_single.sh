#!/usr/bin/env bash

rm movie_exp/scenes/*
python3 scripts/movie_plot/generate_instructions_single.py

# generate story body
python3 dino.py \
 --output_dir movie_exp/scenes \
 --task_file movie_exp/scenes/plot-scene.json \
 --num_entries_per_label 30 \
 --min_num_tokens 50 \
 --max_output_length 100 \
 --top_k 30 \
 --keep_outputs_without_eos \
 --allow_newlines_in_outputs \
 --batch_size 10 \
 --ignore_eos

python3 scripts/movie_plot/post_process.py --task scene

# generate story end
python3 dino.py \
 --output_dir movie_exp/scenes \
 --task_file movie_exp/scenes/final-plot-scene.json \
 --input_file movie_exp/scenes/plot-scene-dataset.jsonl \
 --input_file_type jsonl \
 --num_entries_per_input_and_label 10 \
 --min_num_tokens 10 \
 --max_output_length 50 \
 --top_k 30 \
 --allow_newlines_in_outputs

python3 scripts/movie_plot/post_process.py --task final

python3 scripts/movie_plot/reranking.py --verbose