from algorithm import AlgorithmWithIndexStructure


class IndexHash(AlgorithmWithIndexStructure):

    def get_name(self):
        return "IndexHash"

    __pattern_len = 5

    def init_with_text(self, text):
        self.__text = text
        self.__index = {}

        for i in range(len(self.__text) - IndexHash.__pattern_len + 1):
            substring = self.__text[i:i + IndexHash.__pattern_len]
            if substring in self.__index:
                self.__index[substring].append(i)  # substring already in dictionary
            else:
                self.__index[substring] = [i]  # add to dictionary

    def __init__(self):
        self.__text = ""
        self.__index = {}

    def query(self, pattern):
        if len(pattern) == 0:
            return []

        # include all offsets initially
        results = [x for x in range(0, len(self.__text))]

        # find offsets of each substring in pattern less or equal to default pattern length
        for i in range(0, len(pattern), IndexHash.__pattern_len):
            substring = pattern[i:i + IndexHash.__pattern_len]
            offsets = self.__index[substring] if len(substring) == IndexHash.__pattern_len and substring in self.__index \
                else [item + key.index(substring) for key in filter(lambda x: substring in x, self.__index.keys())
                      for item in self.__index[key]]
            # check if current substring offset is immediately after the previous substring offset
            results = list(filter(lambda x: (x + i) in offsets, results))
            # return if there are no results
            if len(results) == 0:
                break

        results.sort()
        return results
