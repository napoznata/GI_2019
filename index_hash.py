from main import AlgorithmWithIndexStructure
from unit_test import *


class IndexHash(AlgorithmWithIndexStructure):

    def initWithText(self, text):
        self.__text = text

    def __init__(self):
        self.__text = ""
        self.__pattern_len = 0
        self.__index = {}

    def query(self, pattern):
        if len(pattern) == 0:
            return []

        self.__pattern_len = len(pattern)
        self.__index = {}

        for i in range(len(self.__text) - self.__pattern_len + 1):
            substring = self.__text[i:i + self.__pattern_len]
            if substring in self.__index:
                self.__index[substring].append(i)  # substring already in dictionary
            else:
                self.__index[substring] = [i]  # add to dictionary

        return self.__index.get(pattern[:self.__pattern_len], [])


# Run tests
test_results = run_algorithm_tests(IndexHash())
print_test_results(test_results)
