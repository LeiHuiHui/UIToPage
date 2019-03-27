#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import
import sys
import os
from classes.dataset.Generator import *
# from classes.model.pix2code import *
# from classes.model.newpix2code import *
# from classes.model.UItoPage import *
from classes.model.Att_UIToPage import *
from keras.optimizers import adam
import tensorflow as tf
__author__ = 'Hui Lei'

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = "0,1"  # 限制只使用GPU 1

config = tf.ConfigProto()
config.log_device_placement = True
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)


def run(input_path, output_path, is_memory_intensive=False, pretrained_model=None, use_validation_data=False):
    np.random.seed(1234)

    dataset = Dataset()
    # generate_binary_sequences=False 意味着不对partial_sequences进行one-hot编码
    dataset.load(input_path, generate_binary_sequences=False)
    # 生成meta_dataset.npy文件
    dataset.save_metadata(output_path)
    # 生成words.vocab文件
    dataset.voc.save(output_path)

    if not is_memory_intensive:
        dataset.convert_arrays()

        input_shape = dataset.input_shape
        output_size = dataset.output_size

        print(len(dataset.input_images), len(dataset.partial_sequences), len(dataset.next_words))
        print(dataset.input_images.shape, dataset.partial_sequences.shape, dataset.next_words.shape)
    else:
        gui_paths, img_paths = Dataset.load_paths_only(input_path)

        input_shape = dataset.input_shape
        output_size = dataset.output_size
        steps_per_epoch = dataset.size / BATCH_SIZE

        voc = Vocabulary()
        voc.retrieve(output_path)

        generator = Generator.data_generator(voc, gui_paths, img_paths, batch_size=BATCH_SIZE, generate_binary_sequences=False)
        val_generator = None
        validation_steps = None

        # 初始化一个用于validation_data的generator
        if use_validation_data:
            if input_path[-1] == "/":
                val_data_path = os.path.dirname(os.path.dirname(input_path))
            else:
                val_data_path = os.path.dirname(input_path)
            if os.path.exists(val_data_path+"/eval_feature"):
                val_data_path += "/eval_feature"
            else:
                val_data_path += "/eval_set"
            assert os.path.exists(val_data_path)
            # 计算 validation steps
            val_dataset = Dataset()
            # generate_binary_sequences=True 意味着对partial_sequences进行one-hot编码
            val_dataset.load(val_data_path, generate_binary_sequences=False)
            validation_steps = 1 if val_dataset.size / BATCH_SIZE < 1 else val_dataset.size / BATCH_SIZE

            val_gui_paths, val_img_paths = Dataset.load_paths_only(val_data_path)
            val_generator = Generator.data_generator(voc, val_gui_paths, val_img_paths,
                                                      batch_size=BATCH_SIZE, generate_binary_sequences=False, mode="train")

    # model = pix2code(input_shape, output_size, output_path)
    # model = newpix2code(input_shape, output_size, output_path, dataset.voc.size)
    model = Att_UIToPage(input_shape, output_size, output_path, dataset.voc.size, embedding_size=512)
    model.model.compile(adam(0.001), loss='categorical_crossentropy', metrics=["accuracy"])

    if pretrained_model is not None:
        model.model.load_weights(pretrained_model)

    if not is_memory_intensive:
        history = model.fit(dataset.input_images, dataset.partial_sequences, dataset.next_words)
    else:
        checkpoint = model.make_checkpoint()
        early_stopping = model.earlyStopping_callback()
        tbcallback = model.tensorboard_callback(BATCH_SIZE)
        callbacks_list = [checkpoint, early_stopping, tbcallback]
        # callbacks_list = [checkpoint, tbcallback]
        history = model.fit_generator(generator, steps_per_epoch=steps_per_epoch, val_data=val_generator,
                                      val_steps=validation_steps, callbacks_list=callbacks_list)

    model.train_visualization(history)
    model.save_model_to_json()
    model.model_visualization()
    # for eval
    # model.save_models_for_eval(epoch)

if __name__ == "__main__":
    argv = sys.argv[1:]

    if len(argv) < 2:
        print("Error: not enough argument supplied:")
        print("train.py <input path> <output path> <is memory intensive (default: 0)> <pretrained weights (optional)>")
        exit(0)
    else:
        input_path = argv[0]
        output_path = argv[1]
        use_generator = False if len(argv) < 3 else True if int(argv[2]) == 1 else False
        use_validation = False if len(argv) < 4 else True if int(argv[3]) == 1 else False
        pretrained_weigths = None if len(argv) < 5 else argv[4]

    run(input_path, output_path, is_memory_intensive=use_generator, pretrained_model=pretrained_weigths, use_validation_data=use_validation)
