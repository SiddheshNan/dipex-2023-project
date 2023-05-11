import os
import warnings
import io
import random
import numpy as np
from disease_detect import predict_by_ecg_file_using_cnn, predict_realtime_using_cnn
from flask import Flask, jsonify, request, render_template, send_from_directory, Response
from arduino import ecg_signals, connect_to_arduino, start_read_arduino_thread, stop_arduino, current_index, get_current_index
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


warnings.filterwarnings("ignore")
np.set_printoptions(suppress=True)

static_path = os.path.join(os.path.dirname(__file__), 'static')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'



###################################################################################


@app.route('/')
@app.route('/index.html')
def index_page():
    return render_template('index.html')


@app.route('/realtime.html')
def realtime():
    return render_template('realtime.html')


@app.route('/about_project.html')
def about_project():
    return render_template('about_project.html')


@app.route('/guided_by.html')
def guided_by():
    return render_template('guided_by.html')


@app.route('/technology_used.html')
def technology_used():
    return render_template('technology_used.html')


@app.route('/developed_by.html')
def developed_by():
    return render_template('developed_by.html')


@app.route('/<path:path>')
def static_route(path):
    if os.path.isdir(os.path.join(static_path, path)):
        path = os.path.join(path, 'index.html')
    return send_from_directory(static_path, path)


@app.route('/predict', methods=['POST'])
def predict():
    mat_file = request.files['file']
    mat_file_path = os.path.join(app.config['UPLOAD_FOLDER'], mat_file.filename)
    mat_file.save(mat_file_path)
    output_accuracy, output_label = predict_by_ecg_file_using_cnn(mat_file_path)
    return jsonify({'output_label': output_label, 'output_accuracy': output_accuracy})


###################################################################################



@app.route('/get_ecg_signal_img.png')
def get_the_ecg_signal_img():
    try:
        global ecg_signals, get_current_index
        MAX_VALUES = 120

        start = get_current_index() - MAX_VALUES
        end = get_current_index()

        if start < 0:
            start = 0

        print("start: ", start, "end: ", end)

        xpoints = np.array(ecg_signals)

        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)

        axis.plot(xpoints[start:end])

        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)

        return Response(output.getvalue(), mimetype='image/png')

    

    except Exception as e:
        print(e)
        return Response("", mimetype='image/png')



@app.route('/predict_realtime', methods=['GET'])
def predict_realtime_signal():
    ## TODO: normalize the ecg signal
    output_accuracy, output_label = predict_realtime_using_cnn(ecg_signals)
    return jsonify({'output_label': output_label, 'output_accuracy': output_accuracy})


###################################################################################

@app.route('/connect_to_arduino')
def connect_arduino():
    result = connect_to_arduino()
    return jsonify({'msg': result})


@app.route('/start_read_arduino_thread')
def start_arduino_thread():
    result = start_read_arduino_thread()
    return jsonify({'msg': result})


@app.route('/stop_arduino')
def stop_the_arduino():
    result = stop_arduino()
    return jsonify({'msg': result})


###################################################################################


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
