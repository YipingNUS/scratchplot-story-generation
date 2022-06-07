import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, default="story.jsonl",
                        help="The file containing the previous scene.")
    parser.add_argument("--input_dir", type=str, default="movie_exp/scenes/",
                        help="The output directory to which the generated dataset is saved")
    parser.add_argument("--seq_file", type=str, default="plot-summary-dataset.jsonl",
                        help="The file storing the sequence.")
    parser.add_argument("--summary_only", action='store_true', help="If set to true, print only the plot summary.")

    args = parser.parse_args()

    seq_dict = {}
    print("=== Here's the story. Enjoy reading! ===")
    with open(args.input_dir+args.seq_file, "r") as input_file:
        for line in input_file.readlines():
            datum = json.loads(line.strip())
            text = datum['text_a']
            if args.summary_only:
                print(text)
            label = datum['label']
            seq_dict[text] = label

    if not args.summary_only:
        json_list = list()
        with open(args.input_dir+args.input_file, "r") as input_file:
            for line in input_file.readlines():
                datum = json.loads(line.strip())
                text = datum['text_a']
                datum['label'] = seq_dict[text]
                json_list.append(datum)

        json_list = sorted(json_list, key=lambda x: x['label'])

        summaries, full_scenes = [], []
        with open(args.input_dir + args.input_file, "w+") as f:
            for scene in json_list:
                summaries.append(scene['text_a'])
                full_scenes.append(scene['text_b'])
                json.dump(scene, f)
                f.write('\n')
        print("=== Summary ===")
        print(" ".join(summaries))
        print("=== Full Plot ===")
        print(" ".join(full_scenes))
