import machine
import time

def test_pico_health():
    led = machine.Pin("LED", machine.Pin.OUT)

    try:
        for _ in range(5):
            led.on()
            time.sleep(0.1)
            led.off()
            time.sleep(0.1)
        print("LED test: PASSED")

        # Test GPIO pins (example using GP0 and GP1)
        pin_in = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)
        pin_out = machine.Pin(1, machine.Pin.OUT)
        pin_out.on()
        time.sleep(0.1)
        if pin_in.value() == 1:
            print("GPIO test: PASSED")
        else:
            print("GPIO test: FAILED")
        pin_out.off()

        print("All tests completed. If no failures reported, Pico is likely healthy.")

    except Exception as e:
         print(f"An error occurred during testing: {e}")
         print("Pico test: FAILED")
         
test_pico_health()