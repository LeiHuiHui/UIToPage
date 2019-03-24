#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import
__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'

import os
import sys
import hashlib
import shutil

from classes.Sampler import *

argv = sys.argv[1:]

if len(argv) < 1:
    print("Error: not enough argument supplied:")
    print("build_datasets.py <input path> <distribution (default: 6)>")
    exit(0)
else:
    input_path = argv[0]

distribution = 6 if len(argv) < 2 else int(argv[1])

TRAINING_SET_NAME = "training_set"
EVALUATION_SET_NAME = "eval_set"

paths = []
for f in os.listdir(input_path):
    if f.find(".gui") != -1:
        path_gui = "{}/{}".format(input_path, f)
        file_name = f[:f.find(".gui")]

        if os.path.isfile("{}/{}.png".format(input_path, file_name)):
            path_img = "{}/{}.png".format(input_path, file_name)
            paths.append(file_name)

evaluation_samples_number = len(paths) / (distribution + 1)
training_samples_number = evaluation_samples_number * distribution

# training_samples_number = len(paths) / (distribution + 1)
# evaluation_samples_number = training_samples_number * distribution

assert training_samples_number + evaluation_samples_number == len(paths)

print("Splitting datasets, training samples: {}, evaluation samples: {}".format(training_samples_number, evaluation_samples_number))

np.random.shuffle(paths)

eval_set = []
train_set = []

hashes = []
for path in paths:
    if sys.version_info >= (3,):
        f = open("{}/{}.gui".format(input_path, path), 'r', encoding='utf-8')
    else:
        f = open("{}/{}.gui".format(input_path, path), 'r')

    with f:
        chars = ""
        for line in f:
            chars += line
        content_hash = chars.replace(" ", "").replace("\n", "")
        content_hash = hashlib.sha256(content_hash.encode('utf-8')).hexdigest()

        if len(eval_set) == evaluation_samples_number:
            train_set.append(path)
        else:
            is_unique = True
            for h in hashes:
                if h is content_hash:
                    is_unique = False
                    break

            if is_unique:
                eval_set.append(path)
            else:
                train_set.append(path)

        hashes.append(content_hash)

assert len(eval_set) == evaluation_samples_number
assert len(train_set) == training_samples_number

EVALUATION_SET_PATH = "{}/{}".format(os.path.dirname(input_path), EVALUATION_SET_NAME)
TRAINING_SET_PATH = "{}/{}".format(os.path.dirname(input_path), TRAINING_SET_NAME)

if not os.path.exists(EVALUATION_SET_PATH):
    os.makedirs(EVALUATION_SET_PATH)

if not os.path.exists(TRAINING_SET_PATH):
    os.makedirs(TRAINING_SET_PATH)

for path in eval_set:
    shutil.copyfile("{}/{}.png".format(input_path, path), "{}/{}.png".format(EVALUATION_SET_PATH, path))
    shutil.copyfile("{}/{}.gui".format(input_path, path), "{}/{}.gui".format(EVALUATION_SET_PATH, path))

for path in train_set:
    shutil.copyfile("{}/{}.png".format(input_path, path), "{}/{}.png".format(TRAINING_SET_PATH, path))
    shutil.copyfile("{}/{}.gui".format(input_path, path), "{}/{}.gui".format(TRAINING_SET_PATH, path))

print("Training dataset: {}".format(TRAINING_SET_PATH))
print("Evaluation dataset: {}".format(EVALUATION_SET_PATH))
