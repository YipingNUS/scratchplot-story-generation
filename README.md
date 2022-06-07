# Generating Movie Plot with Dino

## Usage

### 1. Generating metadata

Including location, cast, genre and theme.

```bash
sh run_plot_static_gpu.sh
```

### 2. Generate the plot scene by scene

```bash
sh run_plot_dynamic_gpu.sh
```

## Setup

Requires Python3. Tested on Python 3.6 and 3.8.

```bash
pip3 install -r requirements.txt
```

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')

```

### WIP

Generating full scenes from the plot summary. The condition seems weak. 
Temporarily remove it from `run_plot_dynamic_gpu.sh`.

```
# generate the full story
python3 dino.py \
 --output_dir movie_exp/scenes \
 --task_file movie_exp/scenes/plot-final.json \
 --input_file movie_exp/scenes/plot-summary-dataset.jsonl \
 --input_file_type jsonl \
 --num_entries_per_input_and_label 5 \
 --min_num_tokens 5 \
 --max_output_length 200 \
 --top_k 30 \
 --keep_outputs_without_eos \
 --allow_newlines_in_outputs \
 --ignore_eos

python3 scripts/movie_plot/post_process.py --task final --output_file story.jsonl

python3 scripts/movie_plot/print_story.py
```