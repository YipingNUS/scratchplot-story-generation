#!/usr/bin/env bash

rm movie_exp/scenes/*.jsonl
python3 scripts/movie_plot/generate_instructions.py

# scene 1. a bit different from the following.
python3 dino.py \
 --output_dir movie_exp/scenes \
 --task_file movie_exp/scenes/1-plot-scene.json \
 --input_file movie_exp/scenes/plot-scene-dataset.txt \
 --input_file_type plain \
 --num_entries_per_input_and_label 10 \
 --min_num_tokens 5 \
 --max_output_length 100 \
 --top_k 50 \
 --keep_outputs_without_eos \
 --allow_newlines_in_outputs \
 --ignore_eos

python3 scripts/movie_plot/post_process.py --task scene
python3 scripts/movie_plot/shift_scene_backward.py --copy_text_a  --sequence 1


# scene 2. Identical blocks
python3 dino.py \
 --output_dir movie_exp/scenes \
 --task_file movie_exp/scenes/2-plot-scene.json \
 --input_file movie_exp/scenes/plot-scene-dataset.jsonl \
 --input_file_type jsonl \
 --num_entries_per_input_and_label 10 \
 --min_num_tokens 5 \
 --max_output_length 100 \
 --top_k 50 \
 --keep_outputs_without_eos \
 --allow_newlines_in_outputs \
 --ignore_eos

python3 scripts/movie_plot/post_process.py --task scene
python3 scripts/movie_plot/shift_scene_backward.py  --sequence 2

# scene 3. Identical blocks
 python3 dino.py \
 --output_dir movie_exp/scenes \
 --task_file movie_exp/scenes/3-plot-scene.json \
 --input_file movie_exp/scenes/plot-scene-dataset.jsonl \
 --input_file_type jsonl \
 --num_entries_per_input_and_label 10 \
 --min_num_tokens 5 \
 --max_output_length 50 \
 --top_k 50 \
 --keep_outputs_without_eos \
 --allow_newlines_in_outputs \
 --ignore_eos

python3 scripts/movie_plot/post_process.py --task scene
python3 scripts/movie_plot/shift_scene_backward.py  --sequence 3

# scene 4. Identical blocks
python3 dino.py \
 --output_dir movie_exp/scenes \
 --task_file movie_exp/scenes/4-plot-scene.json \
 --input_file movie_exp/scenes/plot-scene-dataset.jsonl \
 --input_file_type jsonl \
 --num_entries_per_input_and_label 10 \
 --min_num_tokens 5 \
 --max_output_length 50 \
 --top_k 50 \
 --keep_outputs_without_eos \
 --allow_newlines_in_outputs \
 --ignore_eos

python3 scripts/movie_plot/post_process.py --task scene
python3 scripts/movie_plot/shift_scene_backward.py  --sequence 4

# scene 5. Identical blocks
python3 dino.py \
 --output_dir movie_exp/scenes \
 --task_file movie_exp/scenes/5-plot-scene.json \
 --input_file movie_exp/scenes/plot-scene-dataset.jsonl \
 --input_file_type jsonl \
 --num_entries_per_input_and_label 10 \
 --min_num_tokens 5 \
 --max_output_length 50 \
 --top_k 50 \
 --keep_outputs_without_eos \
 --allow_newlines_in_outputs \
 --ignore_eos

python3 scripts/movie_plot/post_process.py --task scene
python3 scripts/movie_plot/shift_scene_backward.py  --sequence 5

python3 scripts/movie_plot/print_story.py --summary_only