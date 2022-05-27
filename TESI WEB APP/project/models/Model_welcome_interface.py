import abc
class Model_welcome_interface(abc.ABC):
    '''model interface for each model class method that return the object'''

    @abc.abstractmethod
    def get_random_tip():
        pass