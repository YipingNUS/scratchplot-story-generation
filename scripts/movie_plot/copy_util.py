import json
import argparse


def copy_input(i, input_file=f"plot-scene-batch-input.jsonl", input_dir="movie_exp/", output_file="plot-scene-input.json"):
    """ copy a single line to the input json file for Dino
    :param i: the line number
    :param input_file:
    :param input_dir:
    :param output_file:
    :return: Null
    """
    output_dir = input_dir+"scenes/"
    output_file = output_dir+output_file
    with open(input_dir+input_file, "r") as f:
        lines = f.readlines()
    datum = json.loads(lines[i].strip())
    with open(output_file, "w+", encoding='utf-8') as f:
        json.dump(datum, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Required parameters
    parser.add_argument("--i", type=int, required=True,
                        help="The line number of the json to copy.")
    parser.add_argument("--input_dir", type=str, default="movie_exp/",
                        help="The input directory to which the (previously) generated dataset is saved")
    args = parser.parse_args()

    copy_input(args.i, input_dir=args.input_dir)