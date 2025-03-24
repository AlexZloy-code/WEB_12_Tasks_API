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
zoom_plus, zoom_minus = False, False
left, right, up, down = False, False, False, False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                zoom_plus = True
            if event.key == pygame.K_PAGEDOWN:
                zoom_minus = True
            if event.key == pygame.K_UP:
                up = True
            elif event.key == pygame.K_DOWN:
                down = True
            elif event.key == pygame.K_RIGHT:
                right = True
            elif event.key == pygame.K_LEFT:
                left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_PAGEUP:
                zoom_plus = False
            if event.key == pygame.K_PAGEDOWN:
                zoom_minus = False
            if event.key == pygame.K_UP:
                up = False
            elif event.key == pygame.K_DOWN:
                down = False
            elif event.key == pygame.K_RIGHT:
                right = False
            elif event.key == pygame.K_LEFT:
                left = False

    screen.fill((0, 0, 0))

    if zoom_plus and z < 21:
        z += 1
    elif zoom_minus and z > 1:
        z -= 1

    if up and y < 85:
        y += 1
    elif down and y > -85:
        y -= 1
    elif right and x < 175:
        x += 1
    elif left and x > -175:
        x -= 1

    screen.blit(pygame.image.load(map_edit(x, y, z)), (0, 0))
    clock.tick(50)
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
