#!/usr/bin/env bash
num_stories=100
input_dir=movie_exp/

python3 scripts/movie_plot/generate_instructions_batch.py --num_instructions 300

for i in `seq 0 $num_stories`; do
  rm movie_exp/scenes/*
  python3 scripts/movie_plot/copy_util.py --i $i --input_dir $input_dir
  echo "Generating {$i}th story out of {$num_stories}"
  cat $input_dir/scenes/plot-scene-input.json

  python3 scripts/movie_plot/generate_instructions_single.py --input_file plot-scene-input.json

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

  python3 scripts/movie_plot/append_story.py
done