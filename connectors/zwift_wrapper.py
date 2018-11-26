from zwift import Client

class ZwiftWrapper :
    def __init__ (self, username, password) :
        self.client = Client(username, password)
        self.profile = self.client.get_profile().profile

    def current_zone (self) :
        self.update_profile_maybe()
        return self.get_zone()

    def current_heartrate (self) :
        self.update_profile_maybe()
        return self.heartrate()

    def update_profile_maybe(self):
        if self.profile['worldId'] == None :
            self.profile = self.client.get_profile().profile

    def world(self):
        if self.profile['worldId'] != None :
            return self.client.get_world(self.profile['worldId'])

    def player_status(self):
        return self.world().player_status(self.profile['id'])

    def ftp(self):
        return self.profile['ftp']

    def power(self):
        return self.player_status().power

    def heartrate(self):
        rate = 45
        if self.profile['worldId'] != None :
            rate = self.player_status().heartrate
        if rate == 0 :
            rate = 45
        return rate

    def get_zone(self):
        zone = 1
        if self.profile['worldId'] != None :
            zone = self.zone_from_ratio(self.power() / self.ftp())
        return zone

    def zone_from_ratio(self, ratio):
        zone = 1
        if ratio > 1.2 :
            zone = 6
        elif ratio > 1.05 :
            zone = 5
        elif ratio > 0.9 :
            zone = 4
        elif ratio > 0.75 :
            zone = 3
        elif ratio > 0.55 :
            zone = 2
        return zone
