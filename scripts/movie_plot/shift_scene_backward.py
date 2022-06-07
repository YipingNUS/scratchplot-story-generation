import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Required parameters
    parser.add_argument("--sequence", type=int, default=1,
                        help="The sequence number of the scene.")
    parser.add_argument("--input_file", type=str, default="plot-scene-dataset.jsonl",
                        help="The file containing the previous scene.")
    parser.add_argument("--output_file", type=str, default="plot-summary-dataset.jsonl",
                        help="The file containing the final plot.")
    parser.add_argument("--input_dir", type=str, default="movie_exp/scenes/",
                        help="The input directory to which the generated dataset is saved")
    parser.add_argument("--copy_text_a", action='store_true',
                        help="Whether to copy the text_a field. Only relevant for the first scene", default=False)
    args = parser.parse_args()

    with open(args.input_dir+args.input_file, 'r') as f:
        json_list, output_json_list = list(), list()
        for line in f.readlines():
            datum = json.loads(line.strip())
            prev_scene = datum['text_a']
            next_scene = datum['text_b']
            datum['text_b'] = None
            datum['label'] = args.sequence - 1
            if args.copy_text_a:
                output_json_list.append(datum)

            next_datum = datum.copy()
            next_datum['text_a'] = next_scene
            next_datum['label'] = args.sequence
            json_list.append(next_datum)
            output_json_list.append(next_datum)

    with open(args.input_dir+args.input_file, 'w+') as f:
        for entry in json_list:
            json.dump(entry, f)
            f.write('\n')

    with open(args.input_dir+args.output_file, 'a+') as f:
        for entry in output_json_list:
            json.dump(entry, f)
            f.write('\n')