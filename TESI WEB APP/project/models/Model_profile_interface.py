import abc
class Model_profile_interface(abc.ABC):
    '''model interface for each model class method that return the object'''

    @abc.abstractmethod
    def get_friends(nickname):
        pass
    
    @abc.abstractmethod
    def are_friends(nick, nick_seguito):
        pass

    @abc.abstractmethod
    def insert_follower(nick, nick_seguito):
        pass

    @abc.abstractmethod
    def get_personal_activities(nick):
        pass

    @abc.abstractclassmethod
    def get_ftd_group_by_days(nickname):
        pass

    @abc.abstractclassmethod
    def get_element_and_ftd_group_by_days(nickname):
        pass

    @abc.abstractclassmethod
    def get_element_and_ftd(nickname):
        pass