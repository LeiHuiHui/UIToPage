#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import
import os
import sys
from classes.Sampler import *
# from classes.model.newpix2code import *
from classes.model.UItoPage import *
import numpy as np
from nltk.translate.bleu_score import corpus_bleu

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = "0,1"  # 限制只使用GPU 0


# Read a file and return a string
def load_doc(filename):
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text


def evaluate_model(trained_weights_path, trained_model_name, trained_weights_name, input_path, output_path,search_method="greedy"):
    meta_dataset = np.load("{}/meta_dataset.npy".format(trained_weights_path))
    input_shape = meta_dataset[0]
    output_size = meta_dataset[1]

    # get vocabulary size
    voc = Vocabulary()
    voc.retrieve(weights_path)
    vocabulary_size = voc.size

    model = UItoPage(input_shape, output_size, trained_weights_path, vocabulary_size)
    # model.load(trained_model_name)
    # trained_weights_name 为带后缀名的，如 xx.hdf5
    model.load(name=trained_model_name, weights_name=trained_weights_name)

    sampler = Sampler(trained_weights_path, input_shape, output_size, CONTEXT_LENGTH)

    actual, predicted = list(), list()
    current_num = 0
    for f in os.listdir(input_path):
        if f.find(".gui") != -1:
            file_name = f[:f.find(".gui")]
            evaluation_img = None
            if os.path.isfile("{}/{}.png".format(input_path, file_name)):
                evaluation_img = Utils.get_preprocessed_img("{}/{}.png".format(input_path, file_name), IMAGE_SIZE)

            # 若output_path是提前predict过的所有测试集的结果，则使用已经已有的.gui文件
            if os.path.isfile("{}/{}.gui".format(output_path, file_name)):
                predict_result = load_doc("{}/{}.gui".format(output_path, file_name))
            else:
                if evaluation_img is not None:
                    if search_method == "greedy":
                        result, _ = sampler.predict_greedy(model, np.array([evaluation_img]),require_sparse_label=False)
                        predict_result = result.replace(START_TOKEN, "").replace(END_TOKEN, "")
                        current_num += 1
                        print("Num:{} Evaluate image: {}\n".format(current_num,file_name))
                    else:
                        beam_width = int(search_method)
                        print("Search with beam width: {}".format(beam_width))
                        result, _ = sampler.predict_beam_search(model, np.array([evaluation_img]), beam_width=beam_width, require_sparse_label=False)
                        predict_result =result.replace(START_TOKEN, "").replace(END_TOKEN, "")
                        current_num += 1
                        print("Num:{} Evaluate image: {}\n".format(current_num,file_name))

                    with open("{}/{}.gui".format(output_path, file_name), 'w') as out_f:
                        out_f.write(predict_result)
                else:
                    print("No image exists in input path.")
                    continue

            predict_result = ' '.join(predict_result.split())
            predict_result = predict_result.replace(",", " , ").replace("}", " } ").replace("{", " { ")
            predict_result = predict_result.replace("  ", " ").replace("  ", " ")
            predicted.append(predict_result.split())

            actual_gui = load_doc("{}/{}.gui".format(input_path, file_name))
            actual_gui = ' '.join(actual_gui.split())
            actual_gui = actual_gui.replace(",", " , ").replace("}", " } ").replace("{", " { ")
            actual_gui = actual_gui.replace("  ", " ").replace("  ", " ")
            actual.append([actual_gui.split()])


    assert len(actual) == len(predicted)
    bleu = corpus_bleu(actual, predicted)
    return bleu, actual, predicted

if __name__ == "__main__":
    argv = sys.argv[1:]

    if len(argv) < 4:
        print("Error: not enough argument supplied:")
        print("generate.py <trained weights path> <trained model name> <input image> <output path> <search method (default: greedy)>")
        exit(0)
    else:
        weights_path = argv[0]
        model_name = argv[1]
        weights_name = argv[2]# with .hdf5
        input_path = argv[3]
        output_path = argv[4]
        search_method = "greedy" if len(argv) < 6 else argv[5]

    bleu, actual, predicted = evaluate_model(trained_weights_path=weights_path, trained_model_name=model_name,trained_weights_name=weights_name, input_path=input_path, output_path=output_path, search_method=search_method)
    print(bleu)

