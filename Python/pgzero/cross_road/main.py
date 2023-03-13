import os
import pgzrun
from random import randint, choice


TITLE = 'CROSS THE ROAD'
WIDTH = 480
HEIGHT = 700


def make_car(tracks):
    track = choice(tracks)
    car = Actor(choice(car_names), (43+80*track, randint(100, 700)))
    car.track = track
    tracks.remove(car.track)
    car.speed = randint(1, 10)
    return car, tracks


# Загрузка изображений
roads = [Actor('road', topleft=(80, 0)), Actor('road', topleft=(240, 0))]
grasses = [Actor('grass', topleft=(0, 0)), Actor('grass', topleft=(400, 0))]
chicken = Actor('chicken', (43, 650))
car_names = ['car_white', 'car_blue', 'big_track', 'track',
             'car_yellow', 'car_red', 'car_cyan', 'car_grey']

finsih = Actor('finish', (440, 50))

tracks = [1, 2, 3, 4]
car, tracks = make_car(tracks)
cars = [car]

state = 'game'


def draw():
    for grass in grasses:
        grass.draw()
    for road in roads:
        road.draw()
    for car in cars:
        car.draw()
    finsih.draw()
    chicken.draw()

    if state == 'pause':
        screen.draw.text('PAUSE', fontsize=60,
                         center=(WIDTH//2, HEIGHT//2),
                         color='red')

    if state == 'win':
        screen.draw.text('WIN!', fontsize=60,
                         center=(WIDTH//2, HEIGHT//2),
                         color='green')
    if state == 'loose':
        screen.draw.text('GAME OVER!', fontsize=60,
                         center=(WIDTH//2, HEIGHT//2),
                         color='red')


def update(dt):
    global tracks, state
    if state == 'game':
        if randint(0, 100) < 10:
            if tracks:
                car, tracks = make_car(tracks)
                cars.append(car)

        if keyboard.UP:
            if chicken.y > 40:
                chicken.y -= 5

        if keyboard.DOWN:
            if chicken.y < HEIGHT - 40:
                chicken.y += 5

        for car in cars:
            car.y -= car.speed
            if car.bottom < 0:
                tracks.append(car.track)
                car.track = choice(tracks)
                tracks.remove(car.track)
                car.x = 43+80*car.track
                car.top = 700
                car.image = choice(car_names)
        if chicken.colliderect(finsih):
            state = 'win'
        if chicken.collidelist(cars) != -1:
            state = 'loose'


def on_key_down(key):
    global state
    if state == 'game':
        if key == keys.RIGHT:
            if chicken.x < WIDTH - 43:
                chicken.x += 80
        if key == keys.LEFT:
            if chicken.x > 43:
                chicken.x -= 80
        if key == keys.SPACE:
            state = 'pause'
            return
    if state == 'pause':
        if key == keys.SPACE:
            state = 'game'


pgzrun.go()
