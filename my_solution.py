import sys
import os

import requests
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QLabel, QCheckBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QSize

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 450)
        self.setWindowTitle('Map')
        self.setFocus()
        self.setMouseTracking(True)

        self.x, self.y = 0, 0
        self.z = 1
        self.themes = ['light', 'dark']
        self.theme_image = ['moon.png', 'sun.jpg']
        self.theme = 0
        self.pt = ''

        self.map = QLabel(self)
        self.map.setPixmap(map_edit(self.x, self.y, self.z, self.themes[self.theme], self.pt))

        self.search_result = QLabel(self)
        self.search_result.move(10, 420)
        self.search_result.resize(600, 25)
        self.search_result.setText('Адрес: ')

        self.ask = QLineEdit(self)
        self.ask.move(500, 0)
        self.ask.resize(90, 25)

        self.button_1 = QPushButton(self)
        self.button_1.move(500, 50)
        self.button_1.setText("Искать")
        self.button_1.clicked.connect(self.run)

        self.button_2 = QPushButton(self)
        self.button_2.setIcon(QIcon(f'static/{self.theme_image[self.theme]}'))
        self.button_2.setIconSize(QSize(20, 20))
        self.button_2.move(20, 20)
        self.button_2.clicked.connect(self.run1)

        self.reset_button = QPushButton(self)
        self.reset_button.move(500, 26)
        self.reset_button.setText("Сброс поиска")
        self.reset_button.clicked.connect(self.reset)
        

    def mousePressEvent(self, event):
        self.setFocus()

    def keyPressEvent(self, e):
        if e.key() == 16777220:
            self.run()

        if e.key() == 16777238 and self.z < 21:
            self.z += 1
        elif e.key() == 16777239 and self.z > 1:
            self.z -= 1

        if e.key() == 16777235 and self.y < 85:
            self.y += 1
        elif e.key() == 16777237 and self.y > -85:
            self.y -= 1
        elif e.key() == 16777236 and self.x < 175:
            self.x += 1
        elif e.key() == 16777234 and self.x > -175:
            self.x -= 1

        self.map.setPixmap(map_edit(self.x, self.y, self.z, self.themes[self.theme], self.pt))

    def run(self):
        adress = get_info(self.ask.text())
        self.search_result.setText(f'Адрес: {adress}')

        self.x, self.y = float(pt_edit(self.ask.text()).split(',')[0]), float(pt_edit(self.ask.text()).split(',')[1])
        if mode:
            self.pt = pt_edit(self.ask.text())
        else:
            if not self.pt:
                self.pt = pt_edit(self.ask.text())
            else:
                self.pt += '~' + pt_edit(self.ask.text())
        self.map.setPixmap(map_edit(self.x, self.y, self.z, self.themes[self.theme], self.pt))

    def run1(self):
        self.theme = 1 - self.theme
        self.button_2.setIcon(QIcon(f'static/{self.theme_image[self.theme]}'))
        self.map.setPixmap(map_edit(self.x, self.y, self.z, self.themes[self.theme], self.pt))

    def reset(self):
        if self.pt:
            if mode:
                self.pt = ''
            else:
                self.pt = '~'.join(self.pt.split('~')[:-1])
            self.map.setPixmap(map_edit(self.x, self.y, self.z, self.themes[self.theme], self.pt))
            self.search_result.setText(f'Адрес: ')


def map_edit(x, y, z, theme, pt):
    if pt != '':
        geocoder_params = {
            'll': f'{x},{y}',
            'z': z,
            'pt': pt,
            'l': 'map',
            'theme': theme,
            'api_key': '7712150f-250c-4509-9858-86bcc92fa44b'
        }

        response = requests.get("http://static-maps.yandex.ru/1.x/", params=geocoder_params)

    else:
        geocoder_params = {
            'api_key': '7712150f-250c-4509-9858-86bcc92fa44b',
            'll': f'{x},{y}',
            'z': z,
            'l': 'map',
            'theme': theme
        }

        response = requests.get("http://static-maps.yandex.ru/1.x/", params=geocoder_params)
    map_file = "map.png"
    with open("map.png", "wb") as file:
        file.write(response.content)
    return QPixmap(map_file)


def pt_edit(answer):
    geocoder_params = {
        'apikey': '8013b162-6b42-4997-9691-77b7074026e0',
        'geocode': answer,
        'results': 1,
        'format': 'json'
    }
    
    response = requests.get('http://geocode-maps.yandex.ru/1.x/', params=geocoder_params)
    
    if response:
        json_response = response.json()
        x, y = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
        return f'{x},{y}'
    

def get_info(geo):
    geocoder_params = {
        'apikey': '8013b162-6b42-4997-9691-77b7074026e0',
        'geocode': geo,
        'results': 1,
        'format': 'json'
    }
    
    response = requests.get('http://geocode-maps.yandex.ru/1.x/', params=geocoder_params)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    


if __name__ == '__main__':

    mode = 0 # 0 - показывается много объектов, 1 - показывается 1 объект

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec()
    os.remove('map.png')