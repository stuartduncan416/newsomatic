from gpiozero import MCP3008
import time

while True:
    knobInfo0 = MCP3008(0)
    knobInfo1 = MCP3008(1)
    knobInfo2 = MCP3008(2)
    knobInfo3 = MCP3008(3)
    knobInfo4 = MCP3008(4)

    print("K0: {} \nK1: {}\n K2: {}\n K3: {}\n K4: {}\n".format(knobInfo0.value,knobInfo1.value,knobInfo2.value,knobInfo3.value,knobInfo4.value))

    time.sleep(2)
