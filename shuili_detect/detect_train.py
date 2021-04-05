import os
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import Adam
from keras.utils import multi_gpu_model

import cfg
from network import East
from losses import quad_loss
from data_generator import gen, gen_bootstrap
import os
# os.environ["CUDA_VISIBLE_DEVICES"] = cfg.GPU_NUM
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
sess = tf.Session(config=config)
KTF.set_session(sess)


weights_path = './model/weights_shuiwei_1888T256.008-0.010.h5'
east = East()
east_network = east.east_network()
east_network.summary()
#east_network = multi_gpu_model(east_network, gpus=2)
east_network.compile(loss=quad_loss, optimizer=Adam(lr=cfg.lr,
                                                    # clipvalue=cfg.clipvalue,
                                                    decay=cfg.decay))
if cfg.load_weights and os.path.exists(weights_path):
    east_network.load_weights(weights_path)
    print(weights_path)
    print('#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#')

east_network.fit_generator(generator=gen(is_val=False),
                           steps_per_epoch=cfg.steps_per_epoch,
                           epochs=cfg.epoch_num,
                           validation_data=gen(is_val=True),
                           validation_steps=cfg.validation_steps,
                           verbose=1,
                           initial_epoch=cfg.initial_epoch,
                           callbacks=[
                               EarlyStopping(patience=cfg.patience, verbose=1),
                               ModelCheckpoint(filepath=cfg.model_weights_path,
                                               save_best_only=True,
                                               save_weights_only=False,
                                               verbose=1)])
