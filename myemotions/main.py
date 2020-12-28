from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.graphics import Rectangle
from kivy.properties import StringProperty, ListProperty

import os
import sys

class MyEmotionScale(BoxLayout):
    folder = StringProperty()
    all_folders = ListProperty()
    background_color = ListProperty()

    def get_image(self, value, emotion_type):
        self.background_color = [[0,0.6,0,1],[0.1,0.5,0,1],[0.2,0.4,0,1],[0.3,0.3,0,1],
                                [0.4,0.2,0,1],[0.5,0.1,0,1],[0.6,0,0,1],[0.7,0,0,1],[0.8,0,0,1],[0.9,0,0,1]]
        path = '.'
        value = int(value)
        emotion_type = int(emotion_type)
        self.all_folders = next(os.walk('./img'))[1]
        self.folder = self.all_folders[emotion_type-1]+"/"
        current_image = "img/"+self.folder+str(value)+".png"
        current_emotion = "img/"+self.folder+str(8)+".png"
        return (current_image, current_emotion)

    def save_data(self):
        print("I will save stuff")

    def access_data(self):
        print("I will open data")

class MyEmotionsApp(App):

    def build(self):
        Window.size = 300, 600
        return MyEmotionScale()


if __name__ == '__main__':
    MyEmotionsApp().run()
