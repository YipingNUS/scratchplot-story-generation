import pandas as pd
import json
import os

input_dir = "movie_exp/"
csv_file = "dataset.csv"
content_plan_file = "plot-scene-input.json"
story_file = "plot-scene-best"

csv_path = input_dir+csv_file
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path, encoding='utf-8', low_memory=False)
else:
    print(f"[INFO] Initializing {csv_path}")
    df = pd.DataFrame({"genre": [], "theme": [], "location": [], "actor": [], "actress": [], "story": [], "ending": [], "algorithm": []})

content_plan_path = f"{input_dir}scenes/{content_plan_file}"
with open(content_plan_path, "r", encoding='utf-8') as f:
    input_json = json.load(f)

for algo in ['nsp', 'ppl', 'rank', 'random']:
    story_path = f"{input_dir}scenes/{story_file}-{algo}.json"
    with open(story_path, "r", encoding='utf-8') as f:
        story_json = json.load(f)
    entry = input_json.copy()
    entry['story'] = story_json['text_a']
    entry['ending'] = story_json['text_b']
    entry['algorithm'] = algo
    df = df.append(entry, ignore_index=True)

df.to_csv(csv_path, encoding='utf-8', index=False)

