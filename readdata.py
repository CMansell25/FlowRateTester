import serial

while True:
    # Open serial port (Replace 'COM3' with your serial port)
    ser = serial.Serial('COM3', 9600)

    # Read data from the serial port
    data = ser.read_until().strip()

    # Close the serial port
    ser.close()

    print(data)