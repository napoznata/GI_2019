import abc


class AlgorithmWithIndexStructure(object):

    @abc.abstractmethod
    def init_with_text(self, text):
        pass

    @abc.abstractmethod
    def query(self, pattern):
        pass

    @abc.abstractmethod
    def get_name(self):
        pass
