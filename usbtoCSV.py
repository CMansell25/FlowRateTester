import serial
import csv
import time

serialPort = 'COM5'
baudRate = 115200

ser =serial.Serial(serialPort, baudRate, timeout =1)

csvFile = open('data.csv', mode = 'w', newline = '')
csvWriter = csv.writer(csvFile)

csvWriter.writerow(['Timestamp', 'Data'])

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            csvWriter.writerow([timestamp, line])
            print(f"{timestamp}: {line}")

except KeyboardInterrupt:
    print("Stopping...")

finally:
    ser.close()
    csvFile.close()