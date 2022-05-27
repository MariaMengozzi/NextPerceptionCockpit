import abc
class Model_activity_interface(abc.ABC):
    
    @abc.abstractmethod
    def get_likes_number(id_attivita):
        pass
    
    @abc.abstractclassmethod
    def set_like(id_attivita, nickname):
        pass


    @abc.abstractclassmethod
    def get_results_activity(id_activity):
        pass

    @abc.abstractclassmethod
    def has_like(id_activity, nickname):
        pass

    @abc.abstractclassmethod
    def get_image_from_activity(id_activity):
        pass
    
    @abc.abstractclassmethod
    def get_info_from_id(id_activity):
        pass

    @abc.abstractclassmethod
    def get_elementOfDistraction_data(id_activity):
        pass

    @abc.abstractclassmethod
    def get_FTD_single_activity(id_activity):
        pass