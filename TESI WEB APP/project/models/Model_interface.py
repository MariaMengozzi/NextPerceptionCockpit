import abc
class Model_interface(abc.ABC):
    '''model interface for each model class method that return the object'''

    @abc.abstractmethod
    def get_prova():
        pass