import threading
import serial
import time


ecg_signals = []
ecg_signals_points_length = 1250 # 2500 points ~ 120 seconds
current_index = 0

output = ""

arduino = None
port = 'COM5'


def connect_to_arduino():
    global arduino
    try:
        if arduino == None:
            arduino = serial.Serial(port=port, baudrate=9600)
            return 'connected to arduino'
        else:
            if arduino.isOpen():
                arduino.close()

            arduino.open()
            return "re-connected to arduino"
           
    except serial.SerialException:
        return "failed to connect to arduino"



def flush_arduino():
    global arduino
    arduino.reset_output_buffer()
    arduino.reset_input_buffer()
    arduino.flushInput()
    arduino.flushOutput()


def get_current_index():
    global current_index
    return current_index

def read_arduino():
    global arduino, current_index, ecg_signals, ecg_signals_points_length
    flush_arduino()

    while arduino.isOpen():
        value = arduino.readline().strip().decode("ascii")
        flush_arduino()
        
        if not value or value == "!":
            print("Empty", value)
            time.sleep(0.1)
            continue
        
        value = int(value)


        if current_index + 1 < ecg_signals_points_length:
            ecg_signals.insert(current_index, value)
            current_index += 1

           

        elif current_index + 1 == ecg_signals_points_length:
            print("--------")
            print(ecg_signals)
            print("--------")
            current_index = 0
  
    else:
        print("arduino is not open or has been closed")

    
thread1 = None

def start_read_arduino_thread():
    global thread1
    global arduino


    if arduino == None or not arduino.isOpen():
        return "arduino is not open"
    
    if thread1 == None:
        thread1 = threading.Thread(target=read_arduino)
        thread1.start()
        return "thread started"

    else:
        if thread1.is_alive():
            return "thread already running"
        else:
            thread1 = None
            thread1 = threading.Thread(target=read_arduino)
            thread1.start()
            return "thread started"


def stop_arduino():
    global thread1
    global arduino

    if not arduino.isOpen():
        return "arduino is not open"

    arduino.close()
    time.sleep(0.5)
    return "arduino is closed"