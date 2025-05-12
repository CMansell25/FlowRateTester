from machine import ADC, Pin
import time
import _thread

# --- Pin setup ---
scale_adc = ADC(1)  # GPIO 27 (ADC1)
high_fill_pin = Pin(3, Pin.IN, Pin.PULL_DOWN)
low_fill_pin = Pin(4, Pin.IN, Pin.PULL_DOWN)
relay_pin = Pin(21, Pin.OUT)

# --- Scale constants ---
v_ref = 3.3
r_sense = 150

# --- Shared state ---
relay_state = False
stop_logging = False

def read_scale_weight():
    raw = scale_adc.read_u16()
    voltage = (raw / 65535) * v_ref
    current_mA = (voltage / r_sense) * 1000
    current_mA = max(4, min(current_mA, 20))
    weight = ((current_mA - 4) / 16) * 100
    return round(weight, 2)

def user_input_thread():
    global relay_state, stop_logging
    while True:
        user_input = input("Enter 'on', 'off', or 'stop': ").strip().lower()
        if user_input == "on":
            relay_pin.value(1)
            relay_state = True
            print("Relay turned ON")
        elif user_input == "off":
            relay_pin.value(0)
            relay_state = False
            print("Relay turned OFF")
        elif user_input == "stop":
            stop_logging = True
            print("Stopping logging...")
            break
        else:
            print("Unknown command")

# --- Start user input thread ---
_thread.start_new_thread(user_input_thread, ())

# --- Main logging loop ---
with open("datalog.txt", "a") as log_file:
    log_file.write("Time,Weight,HighFill,LowFill,RelayState\n")
    print("Logging started...")

    while not stop_logging:
        weight = read_scale_weight()
        high_fill = high_fill_pin.value()
        low_fill = low_fill_pin.value()
        log_entry = f"{time.time():.1f},{weight},{high_fill},{low_fill},{relay_state}"
        print(log_entry)
        log_file.write(log_entry + "\n")
        log_file.flush()
        time.sleep(1)

print("Logging finished.")
