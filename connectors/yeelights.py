from time import sleep
from yeelight import *
from yeelight.transitions import *
from yeelight import Flow

class Lights :
    up_duration=1500
    down_duration=2000
    def __init__ (self, ip=None, name=None) :
        if name != None :
            self.bulb = self.find_bulb_by_name(name)
        else :
            self.bulb = self.find_bulb_by_ip(ip)

    def power_on(self):
        self.bulb.turn_on()
        self.bulb.start_music()

    def stop_flow(self) :
        self.bulb.stop_flow()

    def heart_beat_flow (self, rate) :
        down_duration = (60000/rate) - 100
        transitions = [
            RGBTransition(255, 0, 0, duration=50, brightness=100),
            SleepTransition(duration=50),
            RGBTransition(255, 0, 0, duration=down_duration, brightness=1)
            ]
        return Flow(count=0, action=Flow.actions.off, transitions=transitions)

    def sleep_from_rate (self, rate) :
        return 10

    def start_heart_beat (self, rate) :
        return self.bulb.start_flow(self.heart_beat_flow(rate))

    def colour_from_zone (self, zone) :
        return {
            1: {'red': 255,
                'green': 255,
                'blue': 255 },
            2: {'red': 41,
                'green': 116,
                'blue': 254 },
            3: {'red': 76,
                'green': 182,
                'blue': 71 },
            4: {'red': 254,
                'green': 195,
                'blue': 49 },
            5: {'red': 251,
                'green': 79,
                'blue': 45 },
            6: {'red': 252,
                'green': 26,
                'blue': 14 }
            }[zone]

    def speed_from_zone (self, zone) :
        return {
            1: 1,
            2: 0.85,
            3: 0.7,
            4: 0.6,
            5: 0.5,
            6: 0.4
            }[zone]

    def sleep_from_zone(self, zone) :
        return self.speed_from_zone(zone) * self.flow_duration_from_zone(zone) * 0.000001

    def flow_duration_from_zone(self, zone) :
        return self.up_duration * self.down_duration

    def zone_flow (self, zone) :
        colour = self.colour_from_zone(zone)
        speed = self.speed_from_zone(zone)
        transitions = [
            RGBTransition(colour['red'], colour['green'], colour['blue'], duration=self.up_duration*speed, brightness=100),
            RGBTransition(colour['red'], colour['green'], colour['blue'], duration=self.down_duration*speed, brightness=10),
            ]
        return Flow(count=0, action=Flow.actions.off, transitions=transitions)

    def start_zone_flow (self, zone) :
        return self.bulb.start_flow(self.zone_flow(zone))

    def find_bulb_by_name (self, name) :
        bulbs = discover_bulbs()
        bulb = None
        for b in bulbs :
            if b['capabilities']['name'] == name :
                bulb = Bulb(b['ip'])
        return bulb

    def find_bulb_by_ip (self, ip) :
        bulbs = discover_bulbs()
        bulb = None
        for b in bulbs :
            if b['ip'] == ip :
                bulb = Bulb(b['ip'])
        return bulb

    def power_flow(self, zone) :
        self.start_zone_flow(zone)
        sleep(3*self.sleep_from_zone(zone))

    def heart_flow(self, rate) :
        self.start_heart_beat(rate)
        sleep(self.sleep_from_rate(rate))
