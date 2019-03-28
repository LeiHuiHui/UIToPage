from __future__ import absolute_import

import matplotlib.pyplot as plt

from keras.layers import Input, Dense, Dropout, RepeatVector, LSTM, concatenate, Conv2D, Flatten, Embedding, MaxPooling2D, TimeDistributed, Lambda,Reshape
from keras.models import Sequential, Model
from keras.applications.vgg19 import VGG19
from keras.applications.vgg19 import preprocess_input
# from classes.model.kulc.attention import ExternalAttentionRNNWrapper
from kulc.attention import ExternalAttentionRNNWrapper
from keras.optimizers import RMSprop
from keras import *
import keras.backend as K
from .Config import *
from .AModel import *

import numpy as np
from keras.utils import plot_model
import json

W = 14
H = 14
L = W*H
D = 512

class Att_UIToPage(AModel):
    def __init__(self, input_shape, output_size, output_path, vocabulary_size, embedding_size,T=None, D=512):
        AModel.__init__(self, input_shape, output_size, output_path)
        self.name = "Att_UIToPage"

        # vgg19 block5 conv4 (224,224,3)->(14,14,512)->(W,H,D)
        # base_model = VGG19(weights=None, include_top=False)
        # image_model = Model(inputs=base_model.input, outputs=base_model.get_layer('block5_conv3').output)

        
        image_model = Sequential()
        # block 1
        image_model.add(Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=input_shape))
        image_model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
        image_model.add(MaxPooling2D((2, 2), strides=(2, 2)))
        # block 2
        image_model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
        image_model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
        image_model.add(MaxPooling2D((2, 2), strides=(2, 2)))
        # block 3
        image_model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
        image_model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
        image_model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
        image_model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
        image_model.add(MaxPooling2D((2, 2), strides=(2, 2)))
        # block 4
        image_model.add(Conv2D(512, (3, 3), activation='relu', padding='same'))
        image_model.add(Conv2D(512, (3, 3), activation='relu', padding='same'))
        image_model.add(Conv2D(512, (3, 3), activation='relu', padding='same'))
        image_model.add(Conv2D(512, (3, 3), activation='relu', padding='same'))
        image_model.add(MaxPooling2D((2, 2), strides=(2, 2)))
        # block 5
        image_model.add(Conv2D(512, (3, 3), activation='relu', padding='same'))
        image_model.add(Conv2D(512, (3, 3), activation='relu', padding='same'))
        image_model.add(Conv2D(512, (3, 3), activation='relu', padding='same'))
        # image_model.add(Conv2D(512, (3, 3), activation='relu', padding='same'))
        print(image_model.output_shape)
        image_model.add(Reshape((L,D)))
        print(image_model.output_shape)        

        visual_input = Input(shape=input_shape)
        learned_image_features = image_model(visual_input)

        # learned_image_features = np.array(learned_image_features)
        # print(learned_image_features.shape)
        # print(learned_image_features.ndim)

        # K.squeeze(learned_image_features,0)
        print(K.ndim(learned_image_features))
        print(K.shape(learned_image_features))

        # K.reshape(learned_image_features,(-1,14*14,512))
        # print(K.ndim(learned_image_features))
        # print(K.shape(learned_image_features))

        
        # learned_image_features = image_model.predict(visual_input)

        averaged_image_features = Lambda(lambda x: K.mean(x, axis=1))
        averaged_image_features = averaged_image_features(learned_image_features)
        initial_state_h = Dense(embedding_size)(averaged_image_features)
        initial_state_c = Dense(embedding_size)(averaged_image_features)
        encoded_image_features = TimeDistributed(Dense(D, activation="relu"))(learned_image_features)
        print(K.ndim(encoded_image_features))
        print(K.shape(encoded_image_features))

        textual_input = Input(shape=(T,))
        # texts = Embedding(vocab_size+1, 50, input_length=CONTENT_LENGTH, mask_zero=True)(textual_input)
        texts = Embedding(vocabulary_size, embedding_size, input_length=T)(textual_input)

        print(K.ndim(texts))

        encoder = LSTM(embedding_size, return_sequences=True, return_state=True, recurrent_dropout=0.1)
        attented_encoder = ExternalAttentionRNNWrapper(encoder, return_attention=True)
        output = TimeDistributed(Dense(vocabulary_size, activation="softmax"), name="output")

        # for training purpose
        attented_encoder_training_data, _, _ , _= attented_encoder([texts, encoded_image_features], initial_state=[initial_state_h, initial_state_c])
        decoder = output(attented_encoder_training_data)

        # training_model
        self.model = Model(inputs=[visual_input, textual_input], outputs=decoder)

        # optimizer = RMSprop(lr=0.0001, clipvalue=1.0)
        # self.model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        self.initial_state_inference_model = Model(inputs=[learned_image_features], outputs=[initial_state_h, initial_state_c])
        
        inference_initial_state_h = Input(shape=(embedding_size,))
        inference_initial_state_c = Input(shape=(embedding_size,))
        attented_encoder_inference_data, inference_encoder_state_h, inference_encoder_state_c, inference_attention = attented_encoder(
            [texts, encoded_image_features],
            initial_state=[inference_initial_state_h, inference_initial_state_c]
        )
   
        inference_output_data = output(attented_encoder_inference_data)

        self.inference_model = Model(
            inputs=[learned_image_features, textual_input, inference_initial_state_h, inference_initial_state_c],
            outputs=[inference_output_data, inference_encoder_state_h, inference_encoder_state_c, inference_attention]
        )


    def fit(self, images, partial_captions, next_words):
        history = self.model.fit([images, partial_captions], next_words, shuffle=False, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1, validation_split=0.2)
        self.save()
        return history

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
        plt.figure(0)  # 可以自定义图片大小和颜色等
        # 绘制训练损失值
        plt.plot(np.arange(1, EPOCHS+1), history.history['loss'], label="train_loss")
        plt.title('Train loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(loc='upper right')
        # plt.show()
        plt.savefig(self.output_path+"/train_loss.png")
        plt.close(0)

        plt.figure(0)  # 可以自定义图片大小和颜色等
        plt.plot(np.arange(1, EPOCHS+1), history.history['val_acc'], label="eval_acc")
        plt.title('Evaluation accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        # plt.legend(['Train'], loc='upper left')
        plt.legend(loc='lower right')
        # plt.show()
        plt.savefig(self.output_path+"/val_acc.png")
        plt.close(0)

        plt.figure(0)  # 可以自定义图片大小和颜色等
        # 绘制训练 & 验证的准确率值
        plt.plot(np.arange(1, EPOCHS+1), history.history['acc'], label="train_acc")
        plt.plot(np.arange(1, EPOCHS+1), history.history['val_acc'], label="eval_acc")
        plt.title('Train&evaluation accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        # plt.legend(['Train'], loc='upper left')
        plt.legend(loc='lower right')
        # plt.show()
        plt.savefig(self.output_path+"/acc.png")
        plt.close(0)

        plt.figure(0)  # 可以自定义图片大小和颜色等
        # 绘制训练 & 验证的损失值
        plt.plot(np.arange(1, EPOCHS+1), history.history['loss'], label="train_loss")
        plt.plot(np.arange(1, EPOCHS+1), history.history['val_loss'], label="eval_loss")
        plt.title('Train&evaluation loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(loc='upper right')
        # plt.show()
        plt.savefig(self.output_path+"/loss.png")
        plt.close(0)

        plt.figure(0)  # 可以自定义图片大小和颜色等
        # 绘制训练损失值 & 验证准确率值
        plt.plot(np.arange(1, EPOCHS+1), history.history['loss'], label="train_loss")
        plt.plot(np.arange(1, EPOCHS+1), history.history['val_acc'], label="eval_acc")
        plt.title('Train loss&Eval acc')
        plt.ylabel('Loss&Acc')
        plt.xlabel('Epoch')
        plt.legend(loc='upper right')
        # plt.show()
        plt.savefig(self.output_path+"/train_loss and eval_acc.png")
        plt.close(0)

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

    def save_models_for_eval(self, epoch):
        self.inference_model.save("{}/models/sat_inf_{0}.h5".format(self.output_path, epoch))
        self.initial_state_inference_model.save("{}/models/sat_inf_init_{0}.h5".format(self.output_path, epoch))