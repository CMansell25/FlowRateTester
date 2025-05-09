import serial
import pandas as pd
import os
import ast
from datetime import datetime
import threading

class Data:
    def __init__(self) -> None:
        self.data = pd.DataFrame({
            'time' : [],
            'gpm' : []

        })
        self.csvPath = 'C:\\Users\\us2fami0\OneDrive - JE\\Desktop\\Misc\\0-PROJECTS\\GE\\Flowrate Test\\Controller\\data'


    def write(self):
        try:
            full_path = os.path.join(self.csvPath, str(datetime.now().date()) + '.xlsx')
            print(f"Attempting to write to: {full_path}")  # Debugging line
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with pd.ExcelWriter(full_path) as writer:
                self.data.to_excel(writer)
            print("Write successful")  # Debugging line
        except Exception as e:
            print(f"An error occurred: {e}")


            

data = Data()
index = 0

def read_serial(data : Data, stop_event):
    index = 0
    with serial.Serial('COM4', 115200, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1) as s:
        s.flush()
        while not stop_event.is_set():
            lineRead = s.read_until().decode().strip()
            # Check if lineRead is not empty and is a list in string format
            if lineRead and lineRead.startswith('[') and lineRead.endswith(']'):
                # Convert the string representation of a list to an actual list
                data_list = ast.literal_eval(lineRead)
                # Check if the conversion was successful and we have exactly two elements
                if isinstance(data_list, list) and len(data_list) == 2:
                    # Assign the values to the 'time' and 'gpm' columns
                    data.data.loc[index] = {'time': float(data_list), 'gpm': float(data_list)}
                else:
                    print(f"Unexpected data format: {lineRead}")
            else:
                print(f"Invalid data received: {lineRead}")
            print(data.data.loc[index])
            index += 1
            if index % 10 == 0:  # For example, write every 10 data points
                data.write()

data = Data()
stop_event = threading.Event()
serial_thread = threading.Thread(target=read_serial, args=(data, stop_event))

# Start the serial reading thread
serial_thread.start()

# Wait for the user to input the stop command
input("Press Enter to stop the data collection and write to Excel...")
stop_event.set()

# Ensure the thread finishes
serial_thread.join()

# Call the write function one last time to save any remaining data
data.write()



        


    
    




