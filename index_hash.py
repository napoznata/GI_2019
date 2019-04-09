from algorithm import AlgorithmWithIndexStructure
from benchmark import ProgressBar


class IndexHash(AlgorithmWithIndexStructure):

    def get_name(self):
        return "IndexHash"

    __pattern_len = 5

    def init_with_text(self, text):
        self.__text = text
        self.__index = {}

        init_progress = ProgressBar(len(self.__text), "Adding indexes to hash table...")

        for i in range(len(self.__text)):
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
        if len(pattern) == 0:
            return []
        else:
            query_progress = ProgressBar(len(pattern), "Running query...")

            results = []

            # find offsets of each substring in pattern less or equal to default pattern length
            for i in range(0, len(pattern), IndexHash.__pattern_len):
                query_progress.update_progress(i)
                substring = pattern[i:i + IndexHash.__pattern_len]
                if len(substring) == IndexHash.__pattern_len and substring in self.__index:
                    if i == 0:
                        results = list(self.__index[substring])
                    else:
                        # check if current substring offset is immediately after the previous substring offset
                        results = list(filter(lambda x: (x + i) in self.__index[substring], results))
                else:
                    if i == 0:
                        results = [value for key in self.__index.keys() if key.startswith(substring) for value in self.__index[key]]
                    else:
                        results = list(filter(lambda x: self.__text[(x + i):(x + i + len(substring))] == substring, results))

                # return if there are no results
                if len(results) == 0:
                    query_progress.update_progress(len(pattern))
                    break

            query_progress.update_progress(len(pattern))

            sort_progress = ProgressBar(1, 'Sorting result list...')
            results.sort()
            sort_progress.update_progress(1)

            return results
