import pandas as pd
import pickle
from sklearn.preprocessing import Normalizer
from keras.utils.np_utils import to_categorical
from keras import models
from keras import layers

ueg2 = open('data/ueg2_df.pkl', 'rb')
ueg2_df = pickle.load(ueg2)
ueg2.close()

train_data = ueg2_df.values
X = train_data[:, 0:27].astype(float)
Y = train_data[:, 27]
#归一化，返回值为归一化后的数据
X = Normalizer().fit_transform(X)
one_hot_labels = to_categorical(Y)

#模型定义
model = models.Sequential()
model.add(layers.Dense(9400, activation='relu', input_shape=(27,)))
model.add(layers.Dense(9400, activation='relu'))
model.add(layers.Dense(6781,activation='softmax'))
#编译模型
model.compile(optimizer='rmsprop', loss='categorical_crossentropy',metrics=['accuracy'])
X_val = X[:14500]
partial_X_train = X[14500:]
Y_val = one_hot_labels[:14500]
partial_Y_train = one_hot_labels[14500:]
history = model.fit(partial_X_train, partial_Y_train,epochs=10,batch_size=1024,validation_data=(X_val, Y_val))
results = model.evaluate(X, one_hot_labels)