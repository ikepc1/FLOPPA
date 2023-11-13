from time import sleep
from display import Display

def send(lora):
    counter = 0
    print("LoRa Sender")
    display = Display()

    while True:
        payload = "{'#':%d}"%counter
        #print("Sending packet: \n{}\n".format(payload))
        display.display_text("{0}".format(payload))
#         display.display_text("RSSI: {0}".format(lora.packet_rssi()), 0, 55)
        lora.println(payload)

        counter += 1
        sleep(5)