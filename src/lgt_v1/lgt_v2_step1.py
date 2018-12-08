import pandas as pd
import  pickle
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split



ueg = open('data/ueg.pkl', 'rb')
ueg_df = pickle.load(ueg)
ueg.close()

def modify_sampledf(ueg_sample_onehot):
    # tran_list = ['user_id', 'event_id', 'group_id', 'venue_id', 'clock']
    date_deal = []
    for x in ueg_sample_onehot['date']:
        tmp = x.split('-')
        tmp = tmp[0] + tmp[1] + tmp[2]
        date_deal.append(tmp)
    ueg_sample_onehot['date'] = date_deal
    ueg_sample_onehot['date'] = ueg_sample_onehot['date'].astype(float)

    clock_deal = []
    for y in ueg_sample_onehot['clock']:
        tmp = y.replace(':', '')
        clock_deal.append(tmp)
    ueg_sample_onehot['clock'] = clock_deal
    ueg_sample_onehot['clock'] = ueg_sample_onehot['clock'].astype(float)

    tran_list = ['user_id','event_id', 'group_id', 'venue_id']
    for col in tran_list:
        col_float = []
        for i in ueg_sample_onehot[col].values:
            tmp = i[2:]
            col_float.append(tmp)
        col_float = pd.Series(col_float)
        col_float = col_float.astype(float)
        ueg_sample_onehot[col] = col_float

    return ueg_sample_onehot

test_df = modify_sampledf(ueg_df)
train_data = test_df.values
X = train_data[:, 0:25].astype(float)
Y = train_data[:, 25]
one_hot_labels = to_categorical(Y)
one_hot_labels[:,0].any() #为false,故增添了无用的index=0的列
X_train, X_test, Y_train, Y_test = train_test_split(X, one_hot_labels, test_size=0.3, random_state=0)

model = Sequential()
model.add(Dense(1000, activation='relu', input_shape=(25,))) #检查一下
model.add(Dense(8000, activation='relu')) #隐层只控制这个？
model.add(Dense(7193, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

X_val = X_train[:30000]
partial_X_train = X_train[30000:]
Y_val = Y_train[:30000]
partial_Y_train = Y_train[30000:]

history = model.fit(partial_X_train, partial_Y_train,epochs=180,batch_size=2048,validation_data=(X_val, Y_val))