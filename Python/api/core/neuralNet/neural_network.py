#from keras.models import Sequential
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow
import xlrd
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import keras
from tensorflow.keras.models import model_from_json

# Функция для создания необученной нейронной сети (чисто ее архитектуры)
def generate_neural_network_model(input_count, output_count):
    # создаю модель нейронной сети
    model = Sequential()

    # добавляю 4 слоя
    model.add(Dense(3, input_dim=input_count, activation='sigmoid'))
    model.add(Dense(100, activation='sigmoid'))
    model.add(Dense(100, activation='sigmoid'))
    model.add(Dense(output_count, activation='sigmoid'))

    # оптимизатор - способ обучения нейронной сети (adam - самый популярный, а с Дыптан мы проходили SGD - градиентный пуск)
    optimizer = tensorflow.keras.optimizers.Adam(
        learning_rate=0.001,
        beta_1=0.9,
        beta_2=0.999,
        epsilon=1e-07,
        amsgrad=False,
        name="Adam",
    )
    # задаю настройки для обучения (loss - способ измерения ошибки, mse - это среднеквадратичная ошибка)
    model.compile(loss='mse', optimizer=optimizer, metrics=['accuracy'])
    return model


# Функция для создания нейронной сети, и ее сохранения в файл,
# где input_count-количество входов
# output_count
def create_and_save_neural_network(X, Y, input_count, output_count, epochs=100, file_path='model.hdf5'):
    # создаю нейронку с заданной в функции архитектурой нейронной сети
    model = generate_neural_network_model(input_count=input_count, output_count=output_count)
    # обучаю нейронку
    model.fit([X], [Y], epochs=epochs, verbose=2)
    #сохраняю в файл веса нейронки
    model.save_weights(file_path)
    return model


def load_neural_network_model(input_count, output_count, file_path='core/neuralNet/model.hdf5'):
    # создаю архитектуру нейронной сети
    model = generate_neural_network_model(input_count=input_count, output_count=output_count)
    # загружаю веса
    model.load_weights(file_path)
    return model



