import abc

class AlgorithmWithIndexStructure(object):

    @abc.abstractmethod
    def initWithText(self, text):
        pass

    @abc.abstractmethod
    def query(self, pattern):
        pass
