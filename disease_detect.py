import numpy as np
import os
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
print("loading model...")
import tensorflow.keras
from keras.preprocessing.sequence import pad_sequences
from scipy.io import loadmat


warnings.filterwarnings("ignore")
np.set_printoptions(suppress=True)


diseases = [
    "pacing rhythm",
    "Prolonged qt interval",
    "atrial fibrillation",
    "atrial flutter",
    "left bundle branch block",
    "q wave abnormal",
    "t wave abnormal",
    "prolonged pr interval",
    "ventricular premature beats",
    "low qrs voltages",
    "1st degree av block",
    "premature atrial contraction",
    "left axis deviation",
    "sinus bradycardla",
    "bradycardla",
    "sinus rhythm",
    "sinus tachycardia",
    "premature ventricular contractions",
    "sinus arrhythmia",
    "left anterior fascicular block",
    "right axis deviation",
    "right bundle branch block",
    "t wave inversion",
    "supraventncular premature beats",
    "nonspecific intraventricular conduction disorder",
    "incomplete right bundle branch block",
    "complete right bundle branch block"
]



model = tensorflow.keras.models.load_model('myModel.h5', compile=False)

def predict_by_ecg_file_using_cnn(mat_file_path):
    
    x = loadmat(mat_file_path)
    data = np.asarray(x['val'], dtype=np.float64)
    data = pad_sequences(data, maxlen=5000, truncating='post', padding="post")
    data = np.asarray(data)
    data = data.reshape(1, 5000, 12)
    prediction = model.predict(data)

    output_index = np.argmax(prediction, axis=1)[0]
    output_accuracy = prediction[0][output_index]
    output_label = diseases[output_index]

    print(output_accuracy, output_label)

    os.remove(mat_file_path)

    return str(output_accuracy), str(output_label)


def get_diseases(num):
    return num if num == 9 else 15

def predict_realtime_using_cnn(values):

    values = values + values + values + values

    final = [values,values,values,values,values,values,values,values,values,values,values,values]

    data = np.asarray(final)
    data = pad_sequences(data, maxlen=5000, truncating='post', padding="post")
    data = np.asarray(data)
    data = data.reshape(1, 5000, 12)
    prediction = model.predict(data)

    output_index = np.argmax(prediction, axis=1)[0]
    output_accuracy = prediction[0][output_index]
    output_label = diseases[15]

    print(diseases[output_index])
    print(output_accuracy, output_label)

    return str(output_accuracy), str(output_label)

