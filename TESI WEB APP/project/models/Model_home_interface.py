import abc
class Model_home_interface(abc.ABC):
    
    @abc.abstractmethod
    def get_activities(nick):
        pass

    @abc.abstractmethod
    def get_profile_image_from_nick(nick):
        pass

