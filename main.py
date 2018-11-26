import signal
import sys
import random
import os
from connectors.zwift_wrapper import ZwiftWrapper
from connectors.yeelights import Lights

zwift_user_name = os.environ['ZWIFT_USERNAME']
zwift_password = os.environ['ZWIFT_PASSWORD']
led_name = 'desk'
led_ip = '192.168.1.1'

class GracefulKiller:
    bulb = None
    def __init__ (self, lights):
        self.lights = lights
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.lights.stop_flow()
        sys.exit()

def main_loop ():
    lights = Lights(ip=led_ip, name=led_name)
    killer = GracefulKiller(lights)
    zwift = ZwiftWrapper(zwift_user_name, zwift_password)
    lights.power_on()
    counter = 1
    while True:
        counter -= 1
        zone = zwift.current_zone()
        rate = zwift.current_heartrate()
        if counter == 0:
            lights.heart_flow(rate)
            counter = random.randint(20, 30)
        lights.power_flow(zone)

if __name__ == "__main__":
    main_loop()
