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
                        help="The file containing the previous scene.")
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
        args.input_file = f"plot-{task}-dataset.txt"
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
        theme_json = random.choice(theme_json_list)
        genre, theme = theme_json['text_a'], theme_json['text_b']
        locations = list(cast_dict.keys())
        location = random.choice(locations)
        while not cast_dict[location]['actor'] and cast_dict[location]['actress']:
            location = random.choice(locations)
        characters = list()
        actor = random.choice(cast_dict[location]['actor'])
        actress = random.choice(cast_dict[location]['actress'])
        print(f"genre: {genre}\ntheme: {theme}\nLocation: {location}\nCast: {actor} and {actress}")

        if generate_input:
            with open(args.output_dir+args.input_file, "w+") as f:
                f.write(f"{actor} and {actress} met in {location}.")

        with open(args.output_dir + args.output_file, "w+") as f:
            instruction = f"Task: Write a plot summary of a {genre} story " \
                f"featuring {actor} and {actress} in {location} " \
                f"with the main theme \"{theme}\"\n" \
                f"Plot summary: \""
            instruction_json = {"task_name": f"plot-{task}", "labels":
                {"next-scene": {"instruction": instruction, "counter_labels": []}}}
            json.dump(instruction_json, f, indent=2)

        # 1. exposition
        with open(args.output_dir + "1-" + args.output_file, "w+") as f:
            instruction = f"Task: Write a beginning of a {genre} story " \
                f"describing how <X1>\n" \
                f"Story: \""
            instruction_json = {"task_name": f"plot-{task}", "labels":
                {"next-scene": {"instruction": instruction, "counter_labels": []}}}
            json.dump(instruction_json, f, indent=2)

        # 2. rising action
        with open(args.output_dir + "2-" + args.output_file, "w+") as f:
            instruction = f"Task: Write what happens next in a {genre} story " \
                          f"featuring {actor} and {actress} in {location} " \
                          f"with the main theme \"{theme}\"\n" \
                          f"What happened earlier: <X1>\n" \
                          f"What happens next unexpectedly: \""
            instruction_json = {"task_name": f"plot-{task}", "labels":
                {"next-scene": {"instruction": instruction, "counter_labels": []}}}
            json.dump(instruction_json, f, indent=2)

        # 3. climax
        with open(args.output_dir + "3-" + args.output_file, "w+") as f:
            instruction = f"Task: Write what happens next in a {genre} story " \
                f"featuring {actor} and {actress} in {location} " \
                f"with the main theme \"{theme}\"\n" \
                f"What happened earlier: <X1>\n" \
                f"What happens next: \""
            instruction_json = {"task_name": f"plot-{task}", "labels":
                {"next-scene": {"instruction": instruction, "counter_labels": []}}}
            json.dump(instruction_json, f, indent=2)

        # 4. falling action
        with open(args.output_dir + "4-" + args.output_file, "w+") as f:
            instruction = f"Task: Write what happens next in a {genre} story " \
                f"featuring {actor} and {actress} in {location} " \
                f"with the main theme \"{theme}\"\n" \
                f"What happened earlier: <X1>\n" \
                f"What happens next: \""
            instruction_json = {"task_name": f"plot-{task}", "labels":
                {"next-scene": {"instruction": instruction, "counter_labels": []}}}
            json.dump(instruction_json, f, indent=2)

        # 5. resolution
        with open(args.output_dir + "5-" + args.output_file, "w+") as f:
            instruction = f"Task: Write what happens to {actor} and {actress} in the end in a {genre} story.\n" \
                          f"What happened earlier: <X1>\n" \
                          f"What happens in the end: \""
            instruction_json = {"task_name": f"plot-{task}", "labels":
                {"next-scene": {"instruction": instruction, "counter_labels": []}}}
            json.dump(instruction_json, f, indent=2)

        with open(args.output_dir + args.final_output_file, "w+") as f:
            instruction = f"Task: Write a movie scene from a summary for a {genre} movie " \
                f"featuring {actor} and {actress} in {location} " \
                f"with the main theme \"{theme}\"\n" \
                f"Summary : <X1>\n" \
                f"Scene: \""
            instruction_json = {"task_name": f"plot-final", "labels":
                {"full-story": {"instruction": instruction, "counter_labels": []}}}
            json.dump(instruction_json, f, indent=2)