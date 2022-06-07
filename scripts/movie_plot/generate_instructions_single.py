import argparse
import json
from collections import defaultdict
import random

task = "scene"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Required parameters
    parser.add_argument("--cast_file", type=str, default="plot-cast-dataset-clean.jsonl",
                        help="The generated dataset containing location and actor/actress.")
    parser.add_argument("--theme_file", type=str, default="plot-theme-dataset-clean.jsonl",
                        help="The generated dataset countaining the genre and main message of the film.")
    parser.add_argument("--input_file", type=str, default=None,
                        help="The file containing the plot elements (content plan).")
    parser.add_argument("--output_file", type=str, default=None,
                        help="The file containing the instruction.")
    parser.add_argument("--final_output_file", type=str, default=None,
                        help="The file containing the instruction to generate the full story.")
    parser.add_argument("--num_instructions", type=int, default=1,
                        help="The number of instructions to generate")
    parser.add_argument("--input_dir", type=str, default="movie_exp/",
                        help="The input directory to which the (previously) generated dataset is saved")
    parser.add_argument("--output_dir", type=str, default="movie_exp/scenes/",
                        help="The output directory where generated dataset is saved")

    args = parser.parse_args()

    generate_input = False

    if not args.input_file:
        generate_input = True
        args.input_file = f"plot-{task}-input.json"
    if not args.output_file:
        args.output_file = f"plot-{task}.json"
    if not args.final_output_file:
        args.final_output_file = f"plot-final.json"

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

    for i in range(args.num_instructions):
        if generate_input:
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

            with open(args.output_dir+args.input_file, "w+", encoding='utf-8') as f:
                json.dump(input_json, f, ensure_ascii=False, indent=4)
        else:  # input plot elements are provided
            with open(args.output_dir+args.input_file, "r", encoding='utf-8') as f:
                input_json = json.load(f)
                genre, theme, location, actor, actress = input_json['genre'], input_json['theme'], input_json['location'], input_json['actor'], input_json['actress']
        # 1. write the story body
        with open(args.output_dir + args.output_file, "w+") as f:
            instruction = f"Task: Write a plot summary of a {genre} story " \
                f"featuring {actor} and {actress} in {location} " \
                f"with the main theme \"{theme}\"\n" \
                f"Plot summary: \""
            instruction_json = {"task_name": f"plot-{task}", "labels":
                {"next-scene": {"instruction": instruction, "counter_labels": []}}}
            json.dump(instruction_json, f, indent=2)

        # 2. resolution
        with open(args.output_dir + "final-" + args.output_file, "w+") as f:
            instruction = f"Task: Write the ending of a {genre} story. " \
                          f"What happened earlier: <X1>\n" \
                          f"What happens in the end: \""
            instruction_json = {"task_name": f"plot-{task}", "labels":
                {"next-scene": {"instruction": instruction, "counter_labels": []}}}
            json.dump(instruction_json, f, indent=2)
