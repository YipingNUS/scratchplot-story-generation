import argparse
import json
from collections import defaultdict
import random

task = "scene-batch"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Required parameters
    parser.add_argument("--cast_file", type=str, default="plot-cast-dataset-clean.jsonl",
                        help="The generated dataset containing location and actor/actress.")
    parser.add_argument("--theme_file", type=str, default="plot-theme-dataset-clean.jsonl",
                        help="The generated dataset countaining the genre and main message of the film.")
    parser.add_argument("--input_file", type=str, default=None,
                        help="The file containing the previous scene.")
    parser.add_argument("--num_instructions", type=int, default=300,
                        help="The number of instructions to generate")
    parser.add_argument("--input_dir", type=str, default="movie_exp/",
                        help="The input directory to which the (previously) generated dataset is saved")

    args = parser.parse_args()
    if not args.input_file:
        generate_input = True
        args.input_file = f"plot-{task}-input.jsonl"
    print(args)

    cast_dict, theme_json_list = defaultdict(lambda: {"actor": [], "actress": []}), list()

    with open(args.input_dir+args.cast_file, "r") as input_file:
        for line in input_file.readlines():
            datum = json.loads(line.strip())
            label = datum['label']
            location = datum['text_a']
            name = datum['text_b']
            cast_dict[location][label].append(name)

    with open(args.input_dir+args.theme_file, "r") as input_file:
        for line in input_file.readlines():
            datum = json.loads(line.strip())
            theme_json_list.append(datum)

    with open(args.input_dir+args.input_file, "w+", encoding='utf-8') as json_file:
        for i in range(args.num_instructions):
            theme_json = random.choice(theme_json_list)
            genre, theme = theme_json['text_a'], theme_json['text_b']
            locations = list(cast_dict.keys())
            location = random.choice(locations)
            while not cast_dict[location]['actor'] and cast_dict[location]['actress']:
                location = random.choice(locations)
            characters = list()
            actor = random.choice(cast_dict[location]['actor'])
            actress = random.choice(cast_dict[location]['actress'])
            input_json = {"genre": genre, "theme": theme, "location": location, "actor": actor, "actress": actress}
            print(input_json)
            json_file.write(json.dumps(input_json, ensure_ascii=False))
            json_file.write("\n")
