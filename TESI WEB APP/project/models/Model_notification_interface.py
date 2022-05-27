import abc
class Model_notification_interface(abc.ABC):
    

    @abc.abstractmethod
    def insert_new_notification(text, nickname):
        pass
    
    @abc.abstractmethod
    def update_notification(id_notifica):
        pass

    @abc.abstractmethod
    def get_user_notifications(nickname):
        pass