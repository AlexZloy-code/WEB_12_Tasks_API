import os
import argparse
import pygame
import requests


def map_edit(x, y, z):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&z={z}&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        quit()

    map_file = "map.png"
    with open("map.png", "wb") as file:
        file.write(response.content)
    return map_file



parser = argparse.ArgumentParser()
parser.add_argument("--x", type=float, default=30.267808)
parser.add_argument("--y", type=float, default=59.866590)
parser.add_argument("--spn", type=float, default=0.009)
args = parser.parse_args()

x, y, spn = args.x, args.y, args.spn

z = 2

map_file = map_edit(x, y, z)
pygame.init()
pygame.display.set_caption('API 2')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 450))
up, down = False, False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                up = True
            elif event.key == pygame.K_PAGEDOWN:
                down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_PAGEUP:
                up = False
            elif event.key == pygame.K_PAGEDOWN:
                down = False

    screen.fill((0, 0, 0))

    if up and z < 21:
        z += 1

        os.remove(map_file)
        map_file = map_edit(x, y, z)
    elif down and z > 2:
        z -= 1

        os.remove(map_file)
        map_file = map_edit(x, y, z)

    screen.blit(pygame.image.load(map_file), (0, 0))
    clock.tick(60)
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
