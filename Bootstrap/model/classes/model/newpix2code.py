from __future__ import absolute_import

import matplotlib.pyplot as plt

from keras.layers import Input, Dense, Dropout, RepeatVector, LSTM, concatenate, Conv2D, Flatten, Embedding
from keras.models import Sequential, Model
from keras.optimizers import RMSprop
from keras import *
from .Config import *
from .AModel import *

import numpy as np
from keras.utils import plot_model
import json

class newpix2code(AModel):
    def __init__(self, input_shape, output_size, output_path, vocab_size):
        AModel.__init__(self, input_shape, output_size, output_path)
        self.name = "newpix2code"

        image_model = Sequential()
        image_model.add(Conv2D(16, (3, 3), padding='valid', activation='relu', input_shape=input_shape))
        image_model.add(Conv2D(16, (3, 3), activation='relu', padding='same', strides=2))

        image_model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
        image_model.add(Conv2D(32, (3, 3), activation='relu', padding='same', strides=2))

        image_model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
        image_model.add(Conv2D(64, (3, 3), activation='relu', padding='same', strides=2))

        image_model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))

        image_model.add(Flatten())
        image_model.add(Dense(1024, activation='relu'))
        image_model.add(Dropout(0.3))
        image_model.add(Dense(1024, activation='relu'))
        image_model.add(Dropout(0.3))

        image_model.add(RepeatVector(CONTEXT_LENGTH))

        visual_input = Input(shape=input_shape)
        encoded_image = image_model(visual_input)

        textual_input = Input(shape=(CONTEXT_LENGTH,))
        language_model = Embedding(vocab_size+1, 50, input_length=CONTEXT_LENGTH, mask_zero=True)(textual_input)
        language_model = LSTM(128, return_sequences=True)(language_model)
        encoded_text = LSTM(128, return_sequences=True)(language_model)

        decoder = concatenate([encoded_image, encoded_text])

        decoder = LSTM(512, return_sequences=True)(decoder)
        decoder = LSTM(512, return_sequences=False)(decoder)
        decoder = Dense(vocab_size, activation='softmax')(decoder)

        self.model = Model(inputs=[visual_input, textual_input], outputs=decoder)

        optimizer = RMSprop(lr=0.0001, clipvalue=1.0)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    def fit(self, images, partial_captions, next_words):
        history = self.model.fit([images, partial_captions], next_words, shuffle=False, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1, validation_split=0.2)
        self.save()

        # 绘制训练 & 验证的准确率值
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.show()

        # 绘制训练 & 验证的损失值
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.show()

    def fit_generator(self, generator, steps_per_epoch, val_steps, val_data=None, callbacks_list=None):
        history = self.model.fit_generator(generator, steps_per_epoch=steps_per_epoch, epochs=EPOCHS, verbose=2,
                                           validation_data=val_data, validation_steps=val_steps, callbacks=callbacks_list)
        # self.save()
        return history

    def predict(self, image, partial_caption):
        return self.model.predict([image, partial_caption], verbose=0)[0]

    def predict_batch(self, images, partial_captions):
        return self.model.predict([images, partial_captions], verbose=1)

    def train_visualization(self, history):
        plt.style.use("ggplot")
        # plt.figure() 可以自定义图片大小和颜色等
        # 绘制训练损失值
        plt.plot(np.arange(0, EPOCHS), history.history['loss'], label="train_loss")
        plt.title('Train loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(loc='upper right')
        plt.show()

        plt.plot(np.arange(0, EPOCHS), history.history['val_acc'], label="eval_acc")
        plt.title('Evaluation accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        # plt.legend(['Train'], loc='upper left')
        plt.legend(loc='lower right')
        plt.show()

        # 绘制训练 & 验证的准确率值
        plt.plot(np.arange(0, EPOCHS), history.history['acc'], label="train_acc")
        plt.plot(np.arange(0, EPOCHS), history.history['val_acc'], label="eval_acc")
        plt.title('Train&evaluation accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        # plt.legend(['Train'], loc='upper left')
        plt.legend(loc='lower right')
        plt.show()

        # 绘制训练 & 验证的损失值
        plt.plot(np.arange(0, EPOCHS), history.history['loss'], label="train_loss")
        plt.plot(np.arange(0, EPOCHS), history.history['val_loss'], label="eval_loss")
        plt.title('Train&evaluation loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(loc='upper right')
        plt.show()

        # 绘制训练损失值 & 验证准确率值
        plt.plot(np.arange(0, EPOCHS), history.history['loss'], label="train_loss")
        plt.plot(np.arange(0, EPOCHS), history.history['val_acc'], label="eval_acc")
        plt.title('Train loss&Eval acc')
        plt.ylabel('Loss&Acc')
        plt.xlabel('Epoch')
        plt.legend(loc='upper right')
        plt.show()

        # 绘制训练 & 验证的损失值准确率值
        # plt.plot(np.arange(0, EPOCHS), history.history["loss"], label="train_loss")
        # plt.plot(np.arange(0, EPOCHS), history.history["val_loss"], label="val_loss")
        # plt.plot(np.arange(0, EPOCHS), history.history["acc"], label="train_acc")
        # plt.plot(np.arange(0, EPOCHS), history.history["val_acc"], label="val_acc")
        # plt.title("Training Loss and Accuracy on Dataset")
        # plt.xlabel("Epoch")
        # plt.ylabel("Loss/Accuracy")
        # plt.legend(loc="lower right")
        # plt.savefig("../bin/pix2code-bootstrap-1-bin/train_loss_acc.png")
        # plt.show()

        history_json = json.dumps(history.history)
        with open("{}/{}.json".format(self.output_path, "history"), "w") as historyfile:
            historyfile.write(history_json)
        print("history saved")

    def model_visualization(self):
        plot_model(self.model, to_file='{}/model.png'.format(self.output_path), show_shapes=True, show_layer_names=True)
        # ipython notebook 中的可视化实例如下：
        # from IPython.display import SVG
        # from keras.utils.vis_utils import model_to_dot
        # SVG(model_to_dot(model).create(prog='dot', format='svg'))
