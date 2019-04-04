from algorithm import AlgorithmWithIndexStructure
from benchmark import ProgressBar
import bisect


def find_leftmost(index_list, substring):
    return bisect.bisect_left(index_list, substring)


def find_righmost(index_list, substring):
    return bisect.bisect_right(index_list, substring)


class IndexSorted(AlgorithmWithIndexStructure):
    def get_name(self):
        return "IndexSorted"

    __pattern_len = 10

    def __extract_pattern_at(self, index):
        return self.__text[index:index + IndexSorted.__pattern_len]

    def __init__(self):
        self.__text = ""
        self.__index = []

    def init_with_text(self, text):
        self.__text = text
        self.__index = []

        init_progress = ProgressBar(len(self.__text))

        print("Adding substring indexes...")
        for i in range(len(self.__text) + 1):
            self.__index.append((self.__text[i:i + IndexSorted.__pattern_len], i))  # add <substr, offset> pair
            init_progress.update_progress(i)

        print("Sorting index structure...")
        self.__index.sort()  # sort pairs

    def query(self, pattern):
        if len(pattern) == 0:
            return []

        results = []

        query_progress = ProgressBar(len(pattern))

        for i in range(0, len(pattern), IndexSorted.__pattern_len):

            query_progress.update_progress(i)

            substring = pattern[i: i + IndexSorted.__pattern_len]

            index_list = [x[0][:min(len(substring), len(pattern))] for x in self.__index]

            leftmost = find_leftmost(index_list, substring)
            rightmost = find_righmost(index_list, substring)

            if leftmost <= rightmost and self.__index[leftmost][0].startswith(substring):
                result_tuples = self.__index[leftmost:rightmost]
                results = list([x[1] for x in result_tuples])
            # return if there are no results
            if len(results) == 0:
                break

        return sorted(results)
