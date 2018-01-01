import argparse
from init import procedure
import itertools
import sys
import os
from set_manual import resolve
from config import *
import tools

def preprocess(*data_sets, output_dir="training_data"):
    printST(os.path.dirname(data_sets[0]), data_sets)
    output_dir = os.path.join(os.getcwd(), output_dir)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    sgf_files = list(get_files(*data_sets))
    ep = len(sgf_files) * GAME_STEPS
    pos = itertools.chain(*map(get_pos, sgf_files))

    if ep < TESTSET_SIZE * 2:
        pos = list(pos)
        test_size = len(pos) // 3
        test_piece, training_pieces = pos[:test_size], [pos[test_size:]]
    else:
        rand_pos = tools.shuffler(pos)
        test_piece = tools.take_n(TESTSET_SIZE, rand_pos)
        training_pieces = tools.iter_pieces(PIECE_SIZE, rand_pos)

    test_dataset = procedure.rtn_pos(test_piece, is_test=True)
    test_filename = os.path.join(output_dir, "testcv_set.gz")
    print("writing test set...")
    test_dataset.write(test_filename)
    training_datasets = map(procedure.rtn_pos, training_pieces)

    for i, train_dataset in enumerate(training_datasets):
        print("diving %s train set piece..." % i)
        train_filename = os.path.join(output_dir, "train_set%s.gz" % i)
        train_dataset.write(train_filename)

def get_files(*dataset_dirs):
    for dataset_dir in dataset_dirs:
        full_dir = os.path.join(os.getcwd(), dataset_dir)
        dataset_files = [os.path.join(full_dir, name) for name in os.listdir(full_dir)]
        for f in dataset_files:
            if os.path.isfile(f) and f.endswith(".sgf"):
                yield f

def get_pos(file_0):
    with open(file_0) as tf:
        for pos in resolve(tf.read()):
            if pos.is_usable():
                yield pos

def printST(par, dirs):
    print("allocate %s directions of sgf files: \n" % len(dirs))
    print("+--" + par)
    for i, dirname in enumerate(dirs):
        print('|      +--' + os.path.basename(dirname))

parser = argparse.ArgumentParser()
parser.add_argument("input_dir", nargs='+', type=str, help="Unpreprocessed .sgf data directory, required parameter.")
parser.add_argument("--output_dir", type=str, help="Preprocessed output directory, default derectory is ./training_data.")
args = parser.parse_args()
preprocess(*args.input_dir, args.output_dir) if (args.output_dir) else preprocess(*args.input_dir)
