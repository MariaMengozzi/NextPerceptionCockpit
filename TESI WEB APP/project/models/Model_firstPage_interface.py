import abc
class Model_firstPage_interface(abc.ABC):
    '''model interface for each model class method that return the object'''

    @abc.abstractmethod
    def insert_new_user():
        pass

    @abc.abstractmethod
    def get_user_nickname(email):
        pass