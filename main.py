import urllib.request

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window

import wikipedia
import requests
import random

Builder.load_file("frontend.kv")


class FirstScreen(Screen):

    def search_image(self):
        query = self.manager.current_screen.ids.user_query.text

        try:
            page = wikipedia.page(query)
            image_link = page.images[0]
        except wikipedia.exceptions.DisambiguationError as e:
            page = wikipedia.page(random.choice(e.options))
            image_link = page.images[0]
        except wikipedia.exceptions.PageError:
            print("Error....")
            return None  # Return None if there's an error
        except IndexError:
            print("Error....Index")
            return None  # Return None if there's an error

        return image_link

    def get_image(self):
        headers = {'User-agent': 'Mozilla/5.0'}
        url_string = self.search_image()  # Call the method to get the URL
        if not url_string or not url_string.startswith("http"):
            raise ValueError("Invalid URL: URL must start with http or https")

        url = requests.get(url_string, headers=headers)
        image_path = "images/image.jpg"
        urllib.request.urlretrieve(url_string, image_path)

        with open(image_path, "wb") as file:
            file.write(url.content)

        self.manager.current_screen.ids.the_image.source = image_path
        self.manager.current_screen.ids.the_image.reload()


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


Window.fullscreen = 'auto'
MainApp().run()
