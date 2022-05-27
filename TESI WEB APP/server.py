  
#Project Flask MVC

'''__author__ = "mariaMengozzi"
__version__ = "1" '''

from project import app

if __name__ == '__main__':
    app.run(use_reloader=False, port=8000, debug=True) #use_reloader=False-> serve per poter far partire il debug .... , host="localhost"