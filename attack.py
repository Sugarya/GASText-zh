
from common import parse_arguments
from config import *
from datasets import load_data


if __name__ == '__main__':
    args = parse_arguments()
    dataset_name, victim_path = args.dataset, VICTIMS[args.victim]
    origin_examples = load_data(dataset_name)