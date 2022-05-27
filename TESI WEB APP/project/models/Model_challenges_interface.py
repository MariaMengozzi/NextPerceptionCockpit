import abc
class Model_challenges_interface(abc.ABC):
    

    @abc.abstractmethod
    def get_all_challenges():
        pass

    @abc.abstractmethod
    def insert_new_challenge(nome, badge, data_i, data_f):
        pass

    @abc.abstractmethod
    def save_image(img):
        pass

    @abc.abstractmethod
    def send_notification(nome, data_i, data_f):
        pass

    @abc.abstractmethod
    def get_filtered_challenges():
        pass

    @abc.abstractclassmethod
    def insert_partecipazione(id_sfida):
        pass

    @abc.abstractclassmethod
    def get_ranking_challenge(id_challenge):
        pass

    @abc.abstractclassmethod
    def get_challenge_info(id_challenge):
        pass