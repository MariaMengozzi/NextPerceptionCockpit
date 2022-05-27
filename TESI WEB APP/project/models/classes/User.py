#from project.config.Database import connection as con

class User():
    
    def __init__(self, email):
        self.email = email
        self.get_nickname = self.email.replace('@gmail.com', '')
    
    def get_nickname(self):
        return self.get_nickname
    
    def get_email(self):
        return self.email

        