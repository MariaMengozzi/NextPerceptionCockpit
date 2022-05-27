import random
import os


from .Model_welcome_interface import Model_welcome_interface


class Model_welcome(Model_welcome_interface):
    '''implement model interface each method return an object of the relative class'''

    tips = []
    def __init__(self, app):

        with app.open_resource('static/tips.txt', 'rb') as file:
            content = file.read().decode('utf-8')
            self.tips = [line for line in content.splitlines()]



    def get_random_tip(self):
        #print(self.tips, len(self.tips))
        return self.tips[random.randint(0, len(self.tips)-1)]
