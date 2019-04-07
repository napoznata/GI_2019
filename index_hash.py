from algorithm import AlgorithmWithIndexStructure
from benchmark import ProgressBar


class IndexHash(AlgorithmWithIndexStructure):

    def get_name(self):
        return "IndexHash"

    __pattern_len = 5

    def init_with_text(self, text):
        self.__text = text
        self.__index = {}

        ProgressBar.print_message("Adding indexes to hash table...")
        init_progress = ProgressBar(len(self.__text))

        for i in range(len(self.__text) - IndexHash.__pattern_len + 1):
            substring = self.__text[i:i + IndexHash.__pattern_len]
            if substring in self.__index:
                self.__index[substring].append(i)  # substring already in dictionary
            else:
                self.__index[substring] = [i]  # add to dictionary
            init_progress.update_progress(i)

        init_progress.update_progress(len(self.__text))

    def __init__(self):
        self.__text = ""
        self.__index = {}

    def query(self, pattern):
        query_progress = ProgressBar(len(pattern))

        if len(pattern) == 0:
            query_progress.update_progress(len(pattern))
            return []

        # include all offsets initially
        results = [x for x in range(0, len(self.__text))]

        # find offsets of each substring in pattern less or equal to default pattern length
        for i in range(0, len(pattern), IndexHash.__pattern_len):
            query_progress.update_progress(i)
            substring = pattern[i:i + IndexHash.__pattern_len]
            if len(substring) == IndexHash.__pattern_len and substring in self.__index:
                # check if current substring offset is immediately after the previous substring offset
                results = list(filter(lambda x: (x + i) in self.__index[substring], results))
            else:
                results = list(filter(lambda x: self.__text[(x + i):(x + i + len(substring))] == substring, results))

            # return if there are no results
            if len(results) == 0:
                query_progress.update_progress(len(pattern))
                break

        query_progress.update_progress(len(pattern))

        ProgressBar.print_message("Sorting result list...")

        results.sort()
        return results
