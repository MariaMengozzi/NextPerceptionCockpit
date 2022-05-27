import abc
class Model_helper(abc.ABC):
    @abc.abstractclassmethod
    def get_db_manager():
        pass