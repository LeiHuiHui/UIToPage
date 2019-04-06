#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import

import sys

from os.path import basename
from classes.Sampler import *
# from classes.model.pix2code import *
from classes.model.newpix2code import *

import os
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ['CUDA_VISIBLE_DEVICES'] = "0,1"

# def sample(trained_weights_path, trained_model_name, trained_weights_name,input_path,output_path,search_method):
#     meta_dataset = np.load("{}/meta_dataset.npy".format(trained_weights_path))
#     input_shape = meta_dataset[0]
#     output_size = meta_dataset[1]
#     vocabulary_size = meta_dataset[2]

#     # voc = Vocabulary()
#     # voc.retrieve(trained_weights_path)
#     # vocabulary_size = voc.size

#     # model = pix2code(input_shape, output_size, trained_weights_path)
#     model = newpix2code(input_shape, output_size, trained_weights_path, vocabulary_size)
#     # trained_weights_name 为带后缀名的，如 .hdf5
#     model.load(name=trained_model_name, weights_name=trained_weights_name)

#     sampler = Sampler(trained_weights_path, input_shape, output_size, CONTEXT_LENGTH)

#     file_name = basename(input_path)[:basename(input_path).find(".")]
#     evaluation_img = Utils.get_preprocessed_img(input_path, IMAGE_SIZE)

#     if search_method == "greedy":
#         result, _ = sampler.predict_greedy(model, np.array([evaluation_img]),require_sparse_label=False)
#         print("Result greedy: {}".format(result))
#     else:
#         beam_width = int(search_method)
#         print("Search with beam width: {}".format(beam_width))
#         result, _ = sampler.predict_beam_search(model, np.array([evaluation_img]), beam_width=beam_width,require_sparse_label=False)
#         print("Result beam: {}".format(result))

#     with open("{}/{}.gui".format(output_path, file_name), 'w') as out_f:
#         out_f.write(result.replace(START_TOKEN, "").replace(END_TOKEN, ""))


# if __name__ == "__main__":
#     argv = sys.argv[1:]

#     if len(argv) < 4:
#         print("Error: not enough argument supplied:")
#         print("sample.py <trained weights path> <trained model name> <trained_weights_name> <input image> <output path> <search method (default: greedy)>")
#         exit(0)
#     else:
#         trained_weights_path = argv[0]
#         trained_model_name = argv[1]
#         trained_weights_name = argv[2]
#         input_path = argv[3]
#         output_path = argv[4]
#         search_method = "greedy" if len(argv) < 6 else argv[5]
    
#     sample(trained_weights_path=trained_weights_path, trained_model_name=trained_model_name, trained_weights_name=trained_weights_name,input_path=input_path,output_path=output_path,search_method=search_method)
