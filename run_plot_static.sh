#!/usr/bin/env bash

python3 dino.py \
 --model_name gpt2-medium \
 --output_dir movie_exp \
 --task_file movie_task_specs/plot-location.json \
 --num_entries_per_label 10 \
 --min_num_tokens 1 \
 --max_output_length 5 \
 --top_k 30 \
 --batch_size 10 \
 --no_cuda

python3 scripts/movie_plot/post_process.py --task location

python3 dino.py \
 --model_name gpt2-medium \
 --output_dir movie_exp \
 --task_file movie_task_specs/plot-genre.json \
  --num_entries_per_label 10 \
 --min_num_tokens 1 \
 --max_output_length 5 \
 --top_k 30 \
 --batch_size 10 \
 --no_cuda

python3 scripts/movie_plot/post_process.py --task genre

python3 dino.py \
 --model_name gpt2-medium \
 --output_dir movie_exp \
 --task_file movie_task_specs/plot-cast.json \
 --input_file movie_exp/plot-location-dataset-clean.jsonl \
 --input_file_type jsonl \
 --num_entries_per_input_and_label 5 \
 --min_num_tokens 1 \
 --max_output_length 5 \
 --top_k 30 \
 --no_cuda

python3 scripts/movie_plot/post_process.py --task cast

python3 dino.py \
 --model_name gpt2-medium \
 --output_dir movie_exp \
 --task_file movie_task_specs/plot-theme.json \
 --input_file movie_exp/plot-genre-dataset-clean.jsonl \
 --input_file_type jsonl \
 --num_entries_per_input_and_label 5 \
 --min_num_tokens 5 \
 --max_output_length 30 \
 --top_k 30 \
 --no_cuda

python3 scripts/movie_plot/post_process.py --task theme

