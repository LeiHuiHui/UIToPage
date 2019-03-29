__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'

from keras.models import model_from_json
from keras.callbacks import ModelCheckpoint
from keras.callbacks import TensorBoard
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt


class AModel:
    def __init__(self, input_shape, output_size, output_path):
        self.model = None
        self.input_shape = input_shape
        self.output_size = output_size
        self.output_path = output_path
        self.name = ""

    def save(self):
        model_json = self.model.to_json()
        with open("{}/{}.json".format(self.output_path, self.name), "w") as json_file:
            json_file.write(model_json)
        self.model.save_weights("{}/{}.h5".format(self.output_path, self.name))

    def load(self, name="", weights_name=""):
        output_name = self.name if name == "" else name
        weights_name = self.name if weights_name == "" else weights_name
        with open("{}/{}.json".format(self.output_path, output_name), "r") as json_file:
            loaded_model_json = json_file.read()
        self.model = model_from_json(loaded_model_json)
        # self.model.load_weights("{}/{}.h5".format(self.output_path, output_name))
        self.model.load_weights("{}/{}".format(self.output_path, weights_name))

    def save_model_to_json(self):
        model_json = self.model.to_json()
        with open("{}/{}.json".format(self.output_path, self.name), "w") as json_file:
            json_file.write(model_json)
        print("model json saved")

    def make_checkpoint(self):
        filepath = self.output_path + "/weights-improvement-epoch{epoch:02d}-val_acc{val_acc:.4f}-loss{loss:.4f}.hdf5"
        # 中途训练效果提升, 则将文件保存, 每提升一次, 保存一次
        # checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
        checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, mode='max')
        return checkpoint

    def tensorboard_callback(self,batch_size):
        # tbcallback = TensorBoard(log_dir=self.output_path+"/Graph", write_grads=True, histogram_freq=1,write_images=True, batch_size=batch_size)
        tbcallback = TensorBoard(log_dir=self.output_path+"/logs",histogram_freq=0, batch_size=batch_size, write_graph=True, write_grads=False, write_images=False)
        return tbcallback

    def earlyStopping_callback(self):
        earlyStopping = EarlyStopping(monitor="val_acc", mode="max", patience=2, verbose=1)
        return earlyStopping
