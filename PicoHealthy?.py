from machine import Pin, ADC
import time

# Onboard LED (GP25)
led_onboard = Pin(25, Pin.OUT)

# ADC Pins (ADC0 = GP26, ADC1 = GP27, ADC2 = GP28)
adc_pins = [
    {'pin': 26, 'adc': ADC(Pin(26))},
    {'pin': 27, 'adc': ADC(Pin(27))},
    {'pin': 28, 'adc': ADC(Pin(28))}
]


def test_led():
    print("Testing onboard LED (GP25)...")
    for _ in range(5):
        led_onboard.value(1)
        print("LED ON")
        time.sleep(0.5)
        led_onboard.value(0)
        print("LED OFF")
        time.sleep(0.5)
    print("LED test complete.\n")


def test_adc():
    print("Testing ADC pins...")
    for adc_info in adc_pins:
        pin_num = adc_info['pin']
        adc = adc_info['adc']
        print(f"Reading ADC on GP{pin_num}...")
        for _ in range(5):
            value = adc.read_u16()
            print(f"GP{pin_num} ADC value: {value}")
            time.sleep(0.5)
        print(f"ADC GP{pin_num} test complete.\n")


def test_gpio():
    print("Testing GPIO pins 0 to 28...")
    for pin_num in range(29):
        pin = Pin(pin_num, Pin.OUT)
        print(f"Toggling GPIO {pin_num} HIGH")
        pin.value(1)
        time.sleep(0.3)
        print(f"Toggling GPIO {pin_num} LOW")
        pin.value(0)
        time.sleep(0.3)
    print("GPIO test complete.\n")


print("Starting Full Raspberry Pi Pico Health Check...\n")

try:
    test_led()
    test_adc()
    test_gpio()
    print("All tests finished. No errors detected by software.")

except KeyboardInterrupt:
    print("Test stopped by user. Cleaning up...")
    led_onboard.value(0)
