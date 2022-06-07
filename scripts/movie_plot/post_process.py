import argparse
import json
from nltk.corpus import stopwords
from nltk import word_tokenize
from string import punctuation
import re

stop_words = set(stopwords.words('english'))
punctuations = set(punctuation)
punctuations.add(" ")
black_list_scenes = set(['story', 'movie', 'featur', 'theme', 'happen', ':', 'scene', 'plot', 'summary', 'ending', 'point', 'twist', 'lesson', 'spectacle', '@', '<', '>'])
PRONOUN_REGEX = re.compile(r"\b(i|my|me|you|your|we|our)\b")
TASK = "scene"
ending_punctuations = set(['.', '?', '!'])

def __filter_generations(input_file_path: str, output_file_path: str, spec_file_path: str, field="text_a", lower_case=False, remove_punct=False, remove_duplicate=True, filter_pronoun=False, blacklist=None, verbose=False):
    with open(spec_file_path) as json_file:
        spec = json.load(json_file)

    json_list = list()
    unique_values = set()
    with open(input_file_path, "r") as input_file:
        for line in input_file.readlines():
            datum = json.loads(line.strip())
            label = datum['label']
            text = datum[field].lower()

            removed = False
            if field == "text_b":
                instruction = spec["labels"][label]['instruction'] + " " + datum['text_a']
                if datum['text_a'].lower() in datum['text_b'].lower():
                    removed = True
                if filter_pronoun:
                    m = PRONOUN_REGEX.search(datum['text_b'].lower())
                    if m:
                        removed = True
                        msg = f"contains pronoun ({m.group(0)})"
            else:
                instruction = spec["labels"][label]['instruction']
            instruction_words = list(set(word_tokenize(instruction.lower())))
            instruction_words.sort(key=lambda t: len(t), reverse=True)
            for w in instruction_words:
                text = text.replace(w, "")
            remaining_words = [loc for loc in text.split(" ") if len(loc) > 2 and loc not in stop_words]

            # filter by blacklist
            if blacklist:
                for w in blacklist:
                    if w in datum[field].lower():
                        removed = True
                        msg = f"contains blacklist work ({w})"
                        break

            if lower_case:
                datum[field] = datum[field].lower()

            if remove_punct:
                while datum[field]:
                    if datum[field][-1] in punctuations:
                        datum[field] = datum[field][:-1]
                    else:
                        break

            if removed:
                if verbose:
                    print(f"Removing entry: {datum}\n\t because {msg}")
            elif remaining_words:
                if not remove_duplicate or datum[field] not in unique_values:
                    json_list.append(datum)
                    unique_values.add(datum[field])
            elif verbose:
                print(f"Removing entry: {datum} because generating empty content after removing stopwords.")

    with open(output_file_path, 'w+') as outfile:
        for entry in json_list:
            json.dump(entry, outfile)
            outfile.write('\n')


def __filter_scene(input_file_path: str, output_file_path: str, spec_file_path: str, field="text_b", blacklist=black_list_scenes, verbose=False):
    with open(spec_file_path) as json_file:
        spec = json.load(json_file)

    json_list = list()
    with open(input_file_path, "r") as input_file:
        for line in input_file.readlines():
            datum = json.loads(line.strip())
            summary = datum['text_a']
            label = datum['label']
            text = datum[field].lower()

            # filter by blacklist
            instruction = spec["labels"][label]['instruction']
            instruction = instruction[instruction.index("Write"):instruction.index("story")].strip()
            instruction_words = set(word_tokenize(instruction.lower()))
            instruction_words = set([w for w in instruction_words if w not in stop_words])
            instruction_words -= punctuations
            blacklist |= instruction_words
            filtered = False
            for w in blacklist:
                if w in text:
                    filtered = True
                    if verbose:
                        print(f"Removing entry:\t{datum}")
                        print(f"\tGenerated text containing blocked word: {w}")

            # filter by pronouns
            m = PRONOUN_REGEX.search(text)
            if m:
                filtered = True
                if verbose:
                    print(f"Removing entry:\t{datum}")
                    print(f"\tGenerated text containing blocked pronoun: {m.group(0)}")

            # filter by punctuation
            if not text[-1] in ending_punctuations:
                filtered = True
                if verbose:
                    print(f"Removing entry:\t{datum}")
                    print(f"\tNot ending with an acceptable punctuation: {text[-1]}")

            if not filtered:
                json_list.append(datum)

        with open(output_file_path, 'w+') as outfile:
            for scene in json_list:
                json.dump(scene, outfile)
                outfile.write('\n')


def __verify_metadata(text: str, metadata: dict):
    """ verify whether the required metadata fields are present in the generated text
    :param text:
    :param metadata:
    :return: false if pass. true if filtered
    """
    count = 0

    # the location name must appears in the story
    location = metadata['location'].lower()
    if location in text:
        count += 1
    # the actor's first name appears in the story
    actor = metadata['actor'].lower()
    if " " in actor:
        actor = actor[:actor.index(' ')]
    if actor in text:
        count += 1
    # the actress's first name appears in the story
    actress = metadata['actress'].lower()
    if " " in actress:
        actress = actress[:actress.index(' ')]
    if actress in text:
        count += 1
    if count >= 2:  # at least 2 out of (actor, actress, location) appear in the story. -> it's contentful
        return False
    else:  # otherwise, filter the story
        return True


def __filter_story(input_file_path: str, output_file_path: str, spec_file_path: str, metadata_file_path: str,
                   field="text_a", blacklist=black_list_scenes, verbose=False):
    with open(spec_file_path) as json_file:
        spec = json.load(json_file)

    with open(metadata_file_path) as json_file:
        metadata = json.load(json_file)

    json_list = list()
    with open(input_file_path, "r") as input_file:
        for line in input_file.readlines():
            datum = json.loads(line.strip())
            label = datum['label']
            text = datum[field].lower()

            # filter 1: make sure the characters and the location appear in the story
            filtered = __verify_metadata(text, metadata)
            if filtered:
                if verbose:
                    print(f"Removing entry:\t{datum}")
                    print(f"\tBecause doesn't contain metadata: {metadata}")
                continue

            # Filter 2: blacklist words appearing in the instruction
            instruction = spec["labels"][label]['instruction']
            instruction = instruction[instruction.index("Write"):instruction.index("featuring")].strip()
            instruction_words = set(word_tokenize(instruction.lower()))
            instruction_words = set([w for w in instruction_words if w not in stop_words])
            instruction_words -= punctuations
            blacklist |= instruction_words
            for w in blacklist:
                if w in text:
                    filtered = True
                    if verbose:
                        print(f"Removing entry:\t{datum}")
                        print(f"\tBecause out contains blocked word: {w}")
                    break

            # filter by pronouns
            m = PRONOUN_REGEX.search(text)
            if m:
                filtered = True
                if verbose:
                    print(f"Removing entry:\t{datum}")
                    print(f"\tGenerated text containing blocked pronoun: {m.group(0)}")

            if not filtered:
                json_list.append(datum)

        print(f"After filtering, {len(json_list)} entries remain.")
        with open(output_file_path, 'w+') as outfile:
            for scene in json_list:
                json.dump(scene, outfile)
                outfile.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Required parameters
    parser.add_argument("--task", type=str, required=True,
                        help="The postprocessing task to perform: {location, genre, cast, theme, scene}")
    parser.add_argument("--input_file", type=str, default=None,
                        help="The raw generated dataset file.")
    parser.add_argument("--metadata_file", type=str, default=None,
                        help="The json file specify the metadata.")
    parser.add_argument("--output_file", type=str, default=None,
                        help="The filtered dataset file.")
    parser.add_argument("--spec_file", type=str, default=None,
                        help="The spec file used to generate the raw dataset.")
    parser.add_argument("--spec_dir", type=str, default="movie_task_specs/",
                        help="The directory containing the spec files.")
    parser.add_argument("--output_dir", type=str, default="movie_exp/",
                        help="The output directory to which the generated dataset is saved")

    args = parser.parse_args()

    if args.task == "scene":
        args.spec_dir = "movie_exp/scenes/"
        args.output_dir = "movie_exp/scenes/"
        if not args.input_file:
            args.input_file = f"plot-{args.task}-dataset.jsonl"
        if not args.metadata_file:
            args.metadata_file = f"plot-{args.task}-input.json"
        if not args.output_file:
            args.output_file = args.input_file

    if args.task == "final":
        args.spec_dir = "movie_exp/scenes/"
        args.output_dir = "movie_exp/scenes/"
        if not args.input_file:
            args.input_file = f"plot-{TASK}-dataset.jsonl"
        if not args.output_file:
            args.output_file = args.input_file
        if not args.spec_file:
            args.spec_file = f"final-plot-{TASK}.json"

    if not args.input_file:
        args.input_file = f"plot-{args.task}-dataset.jsonl"
    if not args.spec_file:
        args.spec_file = f"plot-{args.task}.json"
    if not args.output_file:
        args.output_file = f"plot-{args.task}-dataset-clean.jsonl"

    print(args)

    if args.task == "location":
        __filter_generations(args.output_dir+args.input_file, args.output_dir+args.output_file, args.spec_dir+args.spec_file, remove_punct=True)
    elif args.task == "genre":
        __filter_generations(args.output_dir+args.input_file, args.output_dir+args.output_file, args.spec_dir+args.spec_file, lower_case=True, remove_punct=True)
    elif args.task == "cast":
        __filter_generations(args.output_dir+args.input_file, args.output_dir+args.output_file, args.spec_dir+args.spec_file, field="text_b", remove_punct=True, remove_duplicate=False)
    elif args.task == "theme":
        __filter_generations(args.output_dir + args.input_file, args.output_dir + args.output_file, args.spec_dir + args.spec_file, field="text_b", remove_duplicate=False, filter_pronoun=True, blacklist=black_list_scenes)
    elif args.task == "scene":
        __filter_story(args.output_dir + args.input_file, args.output_dir+args.output_file, args.spec_dir+args.spec_file, args.output_dir+args.metadata_file, field="text_a")
    elif args.task == "final":
        __filter_scene(args.output_dir + args.input_file, args.output_dir+args.output_file, args.spec_dir+args.spec_file, field="text_b")
    else:
        raise NotImplementedError(f"Task {args.task} not supported!")
