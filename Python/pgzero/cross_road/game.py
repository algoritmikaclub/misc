import json
from random import choice, randint


class Game:
    def __init__(self, Actor):
        self.actor = Actor

    def make_car(self):
        track = choice(self.tracks)
        car = self.actor(choice(self.car_names), (43+track, randint(100, 700)))
        car.track = track
        self.tracks.remove(car.track)
        car.speed = randint(1, 10)
        return car

    def init_lvl(self, lvl):
        with open(f'lvls/lvl{lvl}.json', 'r') as f:
            data = json.load(f)

        self.roads = []
        for coord in data['roads']['coordinates']:
            self.roads.append(self.actor('road', topleft=coord))
        self.grasses = []
        for coord in data['grass']['coordinates']:
            self.grasses.append(self.actor('grass', topleft=coord))
        self.chicken = self.actor('chicken', data['chicken']['coordinates'])
        self.finish = self.actor('flag/1', data['finish']['coordinates'])
        self.finish.time = 0
        self.tracks = data['roads']['tracks']
        self.car_names = data['cars']

        self.cars = []
        for _ in range(len(self.tracks)):        
            car = self.make_car()
            self.cars.append(car)
        