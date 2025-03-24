import os
import argparse
import pygame
import requests


parser = argparse.ArgumentParser()
parser.add_argument("--x", type=float, default=30.267808)
parser.add_argument("--y", type=float, default=59.866590)
parser.add_argument("--spn", type=float, default=0.009)
args = parser.parse_args()

x, y, spn = args.x, args.y, args.spn

map_request = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={spn},0.001&l=map"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    quit()

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
pygame.display.set_caption('API 1')
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)
