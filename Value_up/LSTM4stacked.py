import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, GRU
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import tensorflow as tf
import scipy.io.wavfile as wavf
import os

PATH = 'D:/value_up_dataset/npy'

data = os.listdir(PATH)


def create_dataset(signal_data, look_back=1):
    dataX, dataY = [], []
    for i in range(len(signal_data)-look_back):
        dataX.append(signal_data[i:(i+look_back), 0])
        dataY.append(signal_data[i + look_back, 0])
    return np.array(dataX), np.array(dataY)


class CustomHistory(tf.keras.callbacks.Callback):
    def init(self):
        self.train_loss = []
        self.val_loss = []

    def on_epoch_end(self, batch, logs={}):
        self.train_loss.append(logs.get('loss'))
        self.val_loss.append(logs.get('val_loss'))


# 파일 불러오기 20000만개만 쓰겠음
wav = np.load(PATH + '20min_.npy')[:20000]

# 정규화
scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(np.array(wav).reshape(-1, 1))

# 데이터 나누기, 모델에 사용할 수 있도록 변경하기
train = data[0:15000]
val = data[15000:18000]
test = data[18000:]


look_back = 50
x_train, y_train = create_dataset(train, look_back)
x_val, y_val = create_dataset(val, look_back)
x_test, y_test = create_dataset(test, look_back)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_val = np.reshape(x_val, (x_val.shape[0], x_val.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

model = Sequential()
model.add(GRU(16, batch_input_shape=(1, look_back, 1), return_sequences=True, stateful=True))
model.add(Dropout(0.3))
model.add(GRU(32, batch_input_shape=(1, look_back, 1), return_sequences=True, stateful=True))
model.add(Dropout(0.3))
model.add(GRU(32, batch_input_shape=(1, look_back, 1), return_sequences=True, stateful=True))
model.add(Dropout(0.3))
model.add(GRU(64, batch_input_shape=(1, look_back, 1), stateful=True))
model.add(Dropout(0.3))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')

custom_hist = CustomHistory()
custom_hist.init()

for i in range(5):
    print(f'epoch: {i+1}')
    model.fit(x_train, y_train, epochs=1, batch_size=1, shuffle=False,
              callbacks=[custom_hist], validation_data=(x_val, y_val))
    model.save(f'D://value_up_model//GRU_{i}')
    model.reset_states()

# 7. 모델 사용하기, 예측량: look ahead
look_ahead = 20000
x_hat = x_test[0]
predictions = np.zeros((look_ahead, 1))

for i in range(look_ahead):
    if i % 1000 == 0:
        print('-------------', i, '-------------')
    prediction = model.predict(np.array([x_hat]), batch_size=1)
    predictions[i] = prediction
    x_hat = np.vstack([x_hat[1:], prediction])

# 예측한 것 중 250개만 확인하기
plt.figure(figsize=(12, 5))
plt.plot(np.arange(250), predictions[:250], 'r', label="prediction")
plt.plot(np.arange(250), y_test[:250], label="test function")
plt.legend()
plt.show()

# 정규화 진행한 값 다시 원래 값 범위로 돌려놓기, 예측한 값 저장하기
predictions = scaler.inverse_transform(predictions)
np.save('predictions2', predictions)

# 저장한 값 wav 파일로 변결하기
path = 'predictions2.npy'
sample = np.load(path).reshape(-1).astype(np.float32) * -1
out_f = 'prediction0816_2.wav'
sample_rate = 500
wavf.write(out_f, sample_rate, sample)

