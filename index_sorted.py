from algorithm import AlgorithmWithIndexStructure
from benchmark import ProgressBar
import bisect

class IndexSorted(AlgorithmWithIndexStructure):
    def get_name(self):
        return "IndexSorted"

    __pattern_len = 10

    def __bisect_left(self, x, lo=0, hi=None):
        a = self.__index

        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.__index[mid][0][:min(len(self.__index[mid][0]), len(x))] < x:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def __bisect_right(self, x, lo=0, hi=None):
        a = self.__index

        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.__index[mid][0][:min(len(self.__index[mid][0]), len(x))]  > x:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def __extract_pattern_at(self, index):
        return self.__text[index:index + IndexSorted.__pattern_len]

    def __init__(self):
        self.__text = ""
        self.__index = []

    def init_with_text(self, text):
        self.__text = text
        self.__index = []

        init_progress = ProgressBar(len(self.__text) + 1, "Adding substring indexes...")

        for i in range(len(self.__text) + 1):
            self.__index.append((self.__text[i:i + IndexSorted.__pattern_len], i))
            init_progress.update_progress(i)

        init_progress.update_progress(len(self.__text) + 1)

        sort_init_progress = ProgressBar(1, "Sorting index structure...")
        self.__index.sort(key=lambda t:t[0])
        sort_init_progress.update_progress(1)

    def query(self, pattern):
        if len(pattern) == 0:
            return []

        results = []

        query_progress = ProgressBar(len(pattern), "Running query...")

        for i in range(0, len(pattern), IndexSorted.__pattern_len):

            query_progress.update_progress(i)

            substring = pattern[i: i + IndexSorted.__pattern_len]

            leftmost = self.__bisect_left(pattern)
            rightmost = self.__bisect_right(pattern)

            if leftmost < rightmost and self.__index[leftmost][0].startswith(substring):
                result_tuples = self.__index[leftmost:rightmost]
                results = list([x[1] for x in result_tuples])
            # return if there are no results
            if len(results) == 0:
                break

        results.sort()
        return results
